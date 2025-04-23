async def get_auth_token(client, faker) -> dict[str, str]:
    login_payload = {
        "email": faker.email(),
        "password": faker.password(),
    }
    await client.post("/v1/auth", json=login_payload)
    res = await client.post("/v1/auth/login", json=login_payload)
    res_json = res.json()
    assert res.status_code == 200

    return {"Authorization": f"Bearer {res_json['access_token']}"}


async def test_add_patient(client, faker):
    body = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "date_of_birth": faker.date_of_birth().isoformat(),
        "sex_at_birth": "FEMALE"
    }
    res = await client.post("/v1/patients", json=body, headers=await get_auth_token(client, faker))
    assert res.status_code == 201
    data = res.json()["data"]
    assert data["id"] is not None
    assert data["first_name"] == body["first_name"]
    assert data["last_name"] == body["last_name"]
    assert data["date_of_birth"] == body["date_of_birth"]
    assert data["sex_at_birth"] == body["sex_at_birth"]


async def test_add_patient_invalid_attributes(client, faker):
    body = {
        "email": faker.email(),
        "date_of_birth": faker.date_of_birth().isoformat(),
        "sex_at_birth": "FEMALE"
    }
    res = await client.post("/v1/patients", json=body, headers=await get_auth_token(client, faker))
    assert res.status_code == 422


async def test_add_patient_conflict_by_email(client, faker):
    body = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "date_of_birth": faker.date_of_birth().isoformat(),
        "sex_at_birth": "FEMALE"
    }
    await client.post("/v1/patients", json=body, headers=await get_auth_token(client, faker))
    res = await client.post("/v1/patients", json=body, headers=await get_auth_token(client, faker))
    assert res.status_code == 409
