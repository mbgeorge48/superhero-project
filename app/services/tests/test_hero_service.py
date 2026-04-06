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
            "id": "100",
            "name": "Mott Geege",
            "appearance": {
                "gender": "Male",
                "race": "null",
                "height": ["-", "100 cm"],
                "weight": ["- lb", "100 kg"],
                "eye-color": "Green",
                "hair-color": "Blonde",
            },
        }
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(return_value=mock_json)
        mock_response.raise_for_status = MagicMock()

        mock_get.return_value = mock_response
        result = await HeroService.get_hero_by_id("1")

        # Assertions
        assert isinstance(result, Hero)
        assert result.id == "100"
        assert result.name == "Mott Geege"

        appearance = result.appearance
        assert appearance.gender == "Male"
        assert appearance.race == "null"
        assert appearance.height == ["-", "100 cm"]
        assert appearance.weight == ["- lb", "100 kg"]
        assert appearance.eye_color == "Green"
        assert appearance.hair_color == "Blonde"


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

        result = await HeroService.get_hero_by_id("9999")

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

        result = await HeroService.get_hero_by_id("1")

        assert result is None
