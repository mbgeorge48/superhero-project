import httpx
from bs4 import BeautifulSoup

from app.schemas.hero import HeroListItem

SUPER_HERO_API_URL = "https://superheroapi.com/ids.html"

"""
Example element structure
<tr>
    <td>245</td>
    <td>Ethan Hunt</td>
</tr>
"""


class ScraperService:
    @staticmethod
    async def get_all_ids():
        async with httpx.AsyncClient() as client:
            response = await client.get(SUPER_HERO_API_URL)
            soup = BeautifulSoup(response.text, "html.parser")

            heroes: list[HeroListItem] = []
            for row in soup.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    heroes.append(
                        HeroListItem(
                            id=cols[0].text.strip(),
                            name=cols[1].text.strip(),
                        )
                    )
            return heroes
