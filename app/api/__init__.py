from traceback import print_exc

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette.exceptions import HTTPException

from app.api.v1.endpoints import api_router
from settings import settings

api = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    contact={"name": settings.AUTHOR_NAME, "url": settings.AUTHOR_URL, "email": settings.AUTHOR_EMAIL},
)

api.include_router(api_router)
add_pagination(api)


@api.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, str):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.status_code, "error_message": exc.detail},
        )
    elif isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )

    return JSONResponse(
        status_code=exc.status_code, content={"error_code": exc.detail.value, "error_message": exc.detail.phrase}
    )


@api.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:  # noqa
        if settings.DEVELOPER_MODE:
            print_exc()
        else:
            # TODO: Add a error tracking service.
            pass

        return JSONResponse(status_code=500, content={"error_code": 500, "error_message": "Internal Server Error"})
