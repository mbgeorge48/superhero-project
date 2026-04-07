from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.schemas.hero import Hero
from app.services.hero_service import HeroService


@pytest.mark.asyncio
async def test_get_hero_data_using_id__success():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_json = {
            "response": "success",
            "id": "1",
            "name": "A-Bomb",
            "powerstats": {
                "intelligence": "10",
                "strength": "10",
                "speed": "10",
                "durability": "10",
                "power": "10",
                "combat": "10",
            },
            "biography": {
                "full-name": "Richard Milhouse Jones",
                "alter-egos": "No alter egos found.",
                "aliases": ["Rick Jones"],
                "place-of-birth": "Scarsdale, Arizona",
                "first-appearance": "Hulk #1",
                "publisher": "Marvel Comics",
                "alignment": "good",
            },
            "appearance": {
                "gender": "Male",
                "race": "Human",
                "height": ["6'8", "203 cm"],
                "weight": ["980 lb", "441 kg"],
                "eye-color": "Yellow",
                "hair-color": "No Hair",
            },
            "work": {"occupation": "Adventurer", "base": "Mobile"},
            "connections": {"group-affiliation": "Hulkbusters", "relatives": "-"},
            "image": {"url": "https://www.example.com/image.jpg"},
        }
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(return_value=mock_json)
        mock_response.raise_for_status = MagicMock()

        mock_get.return_value = mock_response
        result = await HeroService.get_hero_by_id("1", {})

        assert isinstance(result, Hero)
        assert result.id == "1"
        assert result.name == "A-Bomb"

        appearance = result.appearance
        assert appearance.gender == "Male"
        assert appearance.eye_color == "Yellow"
        assert appearance.hair_color == "No Hair"


@pytest.mark.asyncio
async def test_get_hero_by_id_api_error_message():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={"response": "error", "error": "invalid id"}
        )
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await HeroService.get_hero_by_id("9999", {})

        assert result is None


@pytest.mark.asyncio
async def test_get_hero_by_id_http_status_error():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "404",
                request=httpx.Request("GET", "http://bla-bla-bla"),
                response=httpx.Response(404),
            )
        )
        mock_get.return_value = mock_response

        result = await HeroService.get_hero_by_id("1", {})

        assert result is None


@pytest.mark.asyncio
async def test_get_hero_by_id_caching_logic():
    """Verify that the second call for the same ID does not hit the API"""
    hero_id = "1"
    mock_cache = {}

    mock_json = {
        "response": "success",
        "id": "1",
        "name": "A-Bomb",
        "powerstats": {
            "intelligence": "10",
            "strength": "10",
            "speed": "10",
            "durability": "10",
            "power": "10",
            "combat": "10",
        },
        "biography": {
            "full-name": "Richard Milhouse Jones",
            "alter-egos": "No alter egos found.",
            "aliases": ["Rick Jones"],
            "place-of-birth": "Scarsdale, Arizona",
            "first-appearance": "Hulk #1",
            "publisher": "Marvel Comics",
            "alignment": "good",
        },
        "appearance": {
            "gender": "Male",
            "race": "Human",
            "height": ["6'8", "203 cm"],
            "weight": ["980 lb", "441 kg"],
            "eye-color": "Yellow",
            "hair-color": "No Hair",
        },
        "work": {"occupation": "Adventurer", "base": "Mobile"},
        "connections": {"group-affiliation": "Hulkbusters", "relatives": "-"},
        "image": {"url": "https://www.example.com/image.jpg"},
    }

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    with patch("app.services.hero_service.httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.get.return_value = mock_response

        # First call, no cached heroes
        result1 = await HeroService.get_hero_by_id(hero_id, mock_cache)
        assert isinstance(result1, Hero)
        assert result1.name == "A-Bomb"
        assert mock_client_instance.get.call_count == 1
        assert hero_id in mock_cache

        # Second calls should hit the cache
        result2 = await HeroService.get_hero_by_id(hero_id, mock_cache)
        assert isinstance(result2, Hero)
        assert result2.name == "A-Bomb"
        # should still be 1, as we're using the cache
        assert mock_client_instance.get.call_count == 1
        assert result1 is result2
