from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates


from app.services.hero_service import HeroService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def list_heroes(request: Request):
    heroes = request.app.state.hero_index
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"heroes": heroes}
    )


@router.get("/{hero_id}")
async def get_hero_by_id(hero_id: str, request: Request):
    hero = await HeroService.get_hero_by_id(hero_id)
    
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

# TODO: caching

    return templates.TemplateResponse(
        request=request,
        name="hero_detail.html",
        context={"hero": hero}
    )
