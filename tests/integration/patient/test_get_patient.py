from pytest import fixture


@fixture
def new_patient(faker, session):
    from toubib.models.schemas.patient import Patient

    patient = Patient(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        date_of_birth=faker.date_of_birth(),
        sex_at_birth="MALE"
    )
    session.add(patient)
    session.flush()
    return patient


async def test_get_patient(client, new_patient):
    res = await client.get(f"/v1/patients/{new_patient.id}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["id"] == new_patient.id
    assert data["first_name"] == new_patient.first_name
    assert data["last_name"] == new_patient.last_name
    assert data["date_of_birth"] == new_patient.date_of_birth.isoformat()
    assert data["sex_at_birth"] == new_patient.sex_at_birth
