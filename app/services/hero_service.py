import logging

import httpx

from app.core.config import settings
from app.schemas.hero import Hero

logger = logging.getLogger(__name__)


class HeroService:
    # Build the base URL once using settings
    BASE_URL = f"https://superheroapi.com/api/{settings.superhero_api_token}"

    @staticmethod
    async def get_hero_by_id(id: str):
        url = f"{HeroService.BASE_URL}/{id}"

        # We want to follow redirects
        # under the hood it redirects to a slightly different URL
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # Check for the SuperheroAPI specific error format
                if data.get("response") == "error":
                    logger.error(f"API Error: {data.get('error')}")
                    return None

                return Hero(**data)

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected Error: {e}")
                return None
