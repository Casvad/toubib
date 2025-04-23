from fastapi import FastAPI
from fastapi.responses import JSONResponse

from toubib.exceptions.exceptions import EntityNotFoundError, DuplicateKeyException, InvalidArgument, \
    UnauthorizedException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)},
        )

    @app.exception_handler(DuplicateKeyException)
    async def duplicate_key_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=409,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidArgument)
    async def invalid_argument_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=401,
            content={"message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def exception_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=500,
            content={"message": str(exc)},
        )