from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.common.container import Container
from src.adapter.inbound.web import endpoints
from src.common.log import logger
from src.application.domain.service.validation_exception import ValidationException
from src.application.domain.service.handlers import HANDLERS


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[__name__, "src.common.container"])
    event_dispatcher = container.event_dispatcher()
    event_dispatcher.subscribe(HANDLERS)

    fastapi_app = FastAPI()
    fastapi_app.container = container  # type: ignore
    # Allow all origins (for development)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or specify your frontend URL: ["http://localhost:8000"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app.include_router(endpoints.router)

    @fastapi_app.exception_handler(ValueError)
    async def _value_error_handler(
        _request: Request,
        exc: ValueError,
        #   logger: Logger = Provide["logger"] # depedency injection
    ):
        logger.error("ValueError: %s", exc)
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @fastapi_app.exception_handler(ValidationException)
    async def _validation_error_handler(_request: Request, exc: ValidationException):
        logger.error("ValidationError: %s", exc)
        return JSONResponse(
            status_code=exc.args[0],
            content={"detail": str(exc.args[1])},
        )

    @fastapi_app.exception_handler(Exception)
    async def _generic_exception_handler(_request: Request, exc: Exception):
        logger.error("Unhandled Exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"},
        )

    return fastapi_app


app = create_app()
