import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.heroes import router as hero_router
from app.services.scraper_service import ScraperService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Scraping heroes")
    app.state.hero_index = await ScraperService.get_all_ids()
    yield

    # On app exit, clear the cache
    app.state.hero_index.clear()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(hero_router, prefix="/heroes")
