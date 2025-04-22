from fastapi import APIRouter
from structlog import get_logger

log = get_logger()
router = APIRouter(prefix="/v1/patients", tags=["Patients"])


@router.get("")
def list_patients():
    pass


@router.post("")
def create_patient():
    pass


@router.get("/{patient_id}")
def get_patient():
    pass
