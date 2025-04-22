from structlog import get_logger
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqla import Item, Session

from toubib.models.entities.doctor import DoctorModel, DoctorIn
from toubib.models.schemas.doctor import Doctor

log = get_logger()
router = APIRouter(prefix="/v1/doctors", tags=["Doctors"])

@router.post("", response_model=Item[DoctorModel], status_code=201)
def create_doctor(*, body: DoctorIn, session: Session = Depends()):
    doctor = Doctor(**body.dict())
    session.add(doctor)
    session.flush()
    return {"data": doctor}


@router.get("/{doctor_id}", response_model=Item[DoctorModel])
def get_doctor(*, doctor_id: int, session: Session = Depends()):
    doctor = session.get(Doctor, doctor_id)
    if doctor is None:
        raise HTTPException(404)
    return {"data": doctor}