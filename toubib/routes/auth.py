from fastapi import APIRouter, Depends
from fastapi_sqla import Session
from structlog import get_logger

from toubib.models.entities.user import UserIn
from toubib.services import user_service, auth_service

log = get_logger()
router = APIRouter(prefix="/v1/auth", tags=["Patients"])


@router.post("/login")
def login(*, body: UserIn, session: Session = Depends()):
    return auth_service.login(body, session)


@router.post("", status_code=201)
def register(*, body: UserIn, session: Session = Depends()):
    return {"data": auth_service.create(body, session)}
