from fastapi import FastAPI
from fastapi.responses import JSONResponse

from toubib.exceptions.exceptions import EntityNotFoundError, DuplicateKeyException, InvalidArgument


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFoundError)
    async def doctor_not_found_exception_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)},
        )

    @app.exception_handler(DuplicateKeyException)
    async def doctor_not_found_exception_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=409,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidArgument)
    async def doctor_not_found_exception_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def doctor_not_found_exception_handler(request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=500,
            content={"message": str(exc)},
        )