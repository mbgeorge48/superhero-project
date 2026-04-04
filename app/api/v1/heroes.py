from fastapi import APIRouter, Request

from app.services.hero_service import HeroService

router = APIRouter()


@router.get("/")
async def list_heroes(request: Request):
    return request.app.state.hero_index


@router.get("/{hero_id}")
async def get_hero_by_id(hero_id: str, request: Request):
    hero = await HeroService.get_hero_by_id(hero_id)

    if not hero:
        return {"error": "Hero not found"}, 404

    return hero
