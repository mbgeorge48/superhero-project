import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.heroes import router as hero_router
from app.core.exceptions import register_exception_handlers
from app.services.scraper_service import ScraperService

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:  [ %(name)s ] - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Scraping heroes")
    raw_hero_data = await ScraperService.get_all_ids()
    app.state.hero_index = {item.id: item for item in raw_hero_data}
    yield

    # On app exit, clear the cache
    app.state.hero_index.clear()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


templates = Jinja2Templates(directory="app/templates")
register_exception_handlers(app, templates)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(hero_router)
