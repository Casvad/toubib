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


async def test_it(client, faker):
    body = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "hiring_date": faker.date(),
        "specialization": faker.bs(),
    }
    headers = await get_auth_token(client, faker)
    res = await client.post("/v1/doctors", json=body, headers=headers)
    assert res.status_code == 201
    data = res.json()["data"]
    assert data["id"] is not None
    assert data["first_name"] == body["first_name"]
    assert data["last_name"] == body["last_name"]
    assert data["hiring_date"] == body["hiring_date"]
    assert data["specialization"] == body["specialization"]
