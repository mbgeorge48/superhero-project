from unittest.mock import AsyncMock, patch

import pytest

from app.services.health_service import HealthService


@pytest.mark.asyncio
async def test_external_api_health_check__success():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = await HealthService.check_external_api_health()

        assert result == {"external_api": "reachable"}


@pytest.mark.asyncio
async def test_external_api_health_check__api_returns_error():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = await HealthService.check_external_api_health()

        assert result == {"external_api": "API responded with error"}


@pytest.mark.asyncio
async def test_external_api_health_check__api_unreachable():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_get.return_value = None

        result = await HealthService.check_external_api_health()

        assert result == {"external_api": "API unreachable"}
