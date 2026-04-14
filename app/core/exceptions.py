import logging

from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def register_exception_handlers(app, templates):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return templates.TemplateResponse(
                request=request,
                name="404.html",
                status_code=404,
                context={
                    "detail": exc.detail,
                    "status_code": 404,
                    "request": request,
                },
            )

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=exc.status_code,
            context={
                "detail": exc.detail,
                "status_code": exc.status_code,
                "request": request,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global Exception: {exc}", exc_info=True)
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=500,
            context={
                "status_code": 500,
                "request": request,
            },
        )
