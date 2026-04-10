from fastapi import APIRouter

from app.services.health_service import HealthService

router = APIRouter()


@router.get("/health")
async def health_check():
    external_health = await HealthService.check_external_api_health()
    return {"status": "healthy", **external_health}
