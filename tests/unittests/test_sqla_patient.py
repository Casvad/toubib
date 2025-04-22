from sqlalchemy.exc import IntegrityError
import pytest

def test_add_patient(session, faker):
    from toubib.models.schemas.patient import Patient

    patient = Patient(
        email=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=faker.date_of_birth(),
        sex_at_birth="FEMALE",
    )
    session.add(patient)
    session.flush()
    assert patient.id is not None

def test_add_patient_trigger_error_by_unique_email(session, faker):
    from toubib.models.schemas.patient import Patient
    email = faker.email()

    patient1 = Patient(
        email=email,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=faker.date_of_birth(),
        sex_at_birth="MALE",
    )
    patient2 = Patient(
        email=email,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=faker.date_of_birth(),
        sex_at_birth="MALE",
    )

    session.add(patient1)
    session.flush()

    session.add(patient2)
    with pytest.raises(IntegrityError):
        session.flush()

    session.rollback()