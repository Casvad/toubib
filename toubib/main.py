from importlib.metadata import version

import fastapi_sqla
from fastapi import FastAPI
from structlog import get_logger

from toubib import routes
from toubib.exceptions.handlers import register_exception_handlers

log = get_logger()

app = FastAPI(title="toubib", version=version("toubib"))

fastapi_sqla.setup(app)

app.include_router(routes.general_router)
app.include_router(routes.patient_router)
app.include_router(routes.doctor_router)

register_exception_handlers(app)