from unittest.mock import AsyncMock, patch

import pytest

from app.services.scraper_service import ScraperService

# Mocked HTML from the ID page
# https://superheroapi.com/ids.html
MOCK_HTML = """
<html>
    <body>
        <table class="table table-striped table-info text-center">
            <thead>
                <tr>
                    <th>#ID</th>
                    <th class="text-center">Chracter Name</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>A-Bomb</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Abe Sapien</td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
"""


@pytest.mark.asyncio
async def test_get_all_ids__success():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = MOCK_HTML
        mock_get.return_value = mock_response

        result = await ScraperService.get_all_ids()

        assert len(result) == 2
        assert result[0].id == "1"
        assert result[0].name == "A-Bomb"
        assert result[1].name == "Abe Sapien"


@pytest.mark.asyncio
async def test_get_all_ids__empty_html():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>No data here</body></html>"
        mock_get.return_value = mock_response

        result = await ScraperService.get_all_ids()

        assert result == []
