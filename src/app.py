from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.container import Container
from src.adapter.inbound.web import endpoints
from src.common.log import logger


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[__name__, "src.common.container"])

    fastapi_app = FastAPI()
    fastapi_app.container = container  # type: ignore
    fastapi_app.include_router(endpoints.router)

    @fastapi_app.exception_handler(ValueError)
    async def value_error_handler(_request: Request, exc: ValueError,
                                #   logger: Logger = Provide["logger"] # depedency injection
                                  ):
        logger.error("ValueError: %s", exc)
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @fastapi_app.exception_handler(Exception)
    async def generic_exception_handler(_request: Request, exc: Exception):
        logger.error("Unhandled Exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"},
        )

    return fastapi_app


app = create_app()
