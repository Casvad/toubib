from fastapi import APIRouter, Depends
from fastapi_sqla import Item, Session
from structlog import get_logger

from toubib.dependencies.auth_dependency import get_current_user
from toubib.models.entities.doctor import DoctorModel, DoctorIn
from toubib.models.entities.user import UserModel
from toubib.services import doctor_service

log = get_logger()
router = APIRouter(prefix="/v1/doctors", tags=["Doctors"])


@router.post("", response_model=Item[DoctorModel], status_code=201)
def create_doctor(*, body: DoctorIn, session: Session = Depends(), current_user: UserModel = Depends(get_current_user)):
    return {"data": doctor_service.create(body, session)}


@router.get("/{doctor_id}", response_model=Item[DoctorModel])
def get_doctor(*, doctor_id: int, session: Session = Depends()):
    return {"data": doctor_service.get_doctor_by_id(doctor_id, session)}
