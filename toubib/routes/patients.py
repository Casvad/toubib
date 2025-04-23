from fastapi import APIRouter, Depends
from fastapi_sqla import Session
from structlog import get_logger

from toubib.dependencies.auth_dependency import get_current_user
from toubib.models.entities.patient import PatientIn
from toubib.models.entities.user import UserModel
from toubib.services import patient_service

log = get_logger()
router = APIRouter(prefix="/v1/patients", tags=["Patients"])


@router.get("")
def list_patients(limit: int = 10, offset: int = 0, session: Session = Depends()):
    return patient_service.get_patients(limit, offset, session)


@router.post("", status_code=201)
def create_patient(*, body: PatientIn, session: Session = Depends(), current_user: UserModel = Depends(get_current_user)):
    return {"data": patient_service.create(body, session)}


@router.get("/{patient_id}")
def get_patient(patient_id: int, session: Session = Depends()):
    return {"data": patient_service.get_patient_by_id(patient_id, session)}
