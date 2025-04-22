from toubib.exceptions.exceptions import EntityNotFoundError
from toubib.models.entities.doctor import DoctorIn, DoctorModel
from toubib.models.schemas.doctor import Doctor
from fastapi_sqla import Session


def create(body: DoctorIn, session: Session) -> DoctorModel:
    doctor = Doctor(**body.dict())
    session.add(doctor)
    session.flush()
    return doctor

def get_doctor_by_id(doctor_id: int, session: Session) -> DoctorModel:
    doctor = session.get(Doctor, doctor_id)
    if doctor is None:
        raise EntityNotFoundError(entity_id=str(doctor_id), entity_type=Doctor)
    return doctor