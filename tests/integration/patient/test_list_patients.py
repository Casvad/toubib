from typing import List

from toubib.models.schemas.patient import Patient


def populate_patients(session, faker, number_of_patients: int) -> List[int]:
    session.query(Patient).delete()
    patient_ids = []
    for _ in range(number_of_patients):
        new_patient = Patient(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.unique.email(),
            date_of_birth=faker.date_of_birth(),
            sex_at_birth="FEMALE"
        )
        session.add(new_patient)
    session.flush()
    return patient_ids


async def test_list_patients_default(client, session, faker):
    populate_patients(session, faker, number_of_patients=5)

    res = await client.get("/v1/patients")
    assert res.status_code == 200
    data = res.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 5


async def test_list_patients_default_20_patients(client, session, faker):
    populate_patients(session, faker, number_of_patients=20)

    res = await client.get("/v1/patients")
    assert res.status_code == 200
    data = res.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 10


async def test_list_patients_with_offset_limit(client, session, faker):
    populate_patients(session, faker, number_of_patients=50)

    res = await client.get("/v1/patients?offset=40&limit=10")
    assert res.status_code == 200
    data = res.json()["data"]
    last_names = list(map(lambda patient: patient["last_name"], data))
    sorted_last_names = sorted(last_names, reverse=True)
    assert isinstance(data, list)
    assert len(data) == 10
    for i in range(len(last_names)):
        assert last_names[i] == sorted_last_names[i]


async def test_list_patients_invalid_params(client):
    res = await client.get("/v1/patients?offset=-5&limit=-1")
    assert res.status_code == 400
