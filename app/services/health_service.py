import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class HealthService:
    URL = f"{settings.superhero_api_base_url}{settings.superhero_api_token}/1"

    @staticmethod
    async def check_external_api_health():
        async with httpx.AsyncClient(follow_redirects=True) as client:

            try:
                # We use a 2-second timeout so the health check doesn't hang
                response = await client.get(HealthService.URL, timeout=2.0)

                if response.status_code == 200:
                    return {"external_api": "reachable"}
                else:
                    return {"external_api": "API responded with error"}

            except Exception:
                return {"external_api": "API unreachable"}
