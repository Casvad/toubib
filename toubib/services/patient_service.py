from fastapi_sqla import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from toubib.exceptions.exceptions import EntityNotFoundError, IllegalStateException, DuplicateKeyException, \
    InvalidArgument
from toubib.models.entities.general import PageOut
from toubib.models.entities.patient import PatientIn, PatientModel
from toubib.models.schemas.patient import Patient


def create(body: PatientIn, session: Session) -> PatientModel:
    patient = Patient(**body.dict())
    try:
        session.add(patient)
        session.flush()
    except IntegrityError as e:
        session.rollback()
        error_message = str(e.orig).lower()
        if 'unique' in str(e.orig).lower():
            raise DuplicateKeyException(error_message, Patient)
        else:
            raise IllegalStateException(f"Unknown error creating patient: {str(e)}", e)
    return patient


def get_patient_by_id(patient_id: int, session: Session) -> PatientModel:
    patient = session.get(Patient, patient_id)
    if patient is None:
        raise EntityNotFoundError(entity_id=str(patient_id), entity_type=Patient)
    return patient

def get_patients(limit: int, offset: int, session: Session) -> PageOut[PatientModel]:

    if limit < 1:
        raise InvalidArgument("limit cannot be negative or 0")
    if offset < 0:
        raise InvalidArgument("offset cannot be negative or 0")

    # this can be cached
    total = session.query(Patient).count()
    patients = session.query(Patient).order_by(desc(Patient.last_name)).offset(offset).limit(limit).all()

    return PageOut[PatientModel](
        data=patients,
        total_data=total,
        offset=offset,
        limit=limit,
    )
