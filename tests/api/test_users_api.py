import pytest


@pytest.mark.asyncio
async def test_create_student_api(client):
    payload = {
        "full_name": "Solar Inverter",
        "email": "solarinverter@gmail.com"
    }
    response = await client.post("/api/v1/users/students/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "solarinverter@gmail.com"
    assert data["role"] == "student"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_create_teacher_api(client):
    payload = {
        "full_name": "Teacha Kelly",
        "email": "teach.kelly@gmail.com"
    }
    response = await client.post("/api/v1/users/teachers/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "teach.kelly@gmail.com"
    assert data["role"] == "teacher"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_get_user_not_found_api(client):
    fake_id = "7cc36b04-13f5-456b-8596-ed331fdaca67"
    response = await client.get(f"/api/v1/users/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_create_student_invalid_email_api(client):
    payload = {
        "full_name": "Bad Email",
        "email": "not-an-email"
    }
    response = await client.post("/api/v1/users/students/", json=payload)
    assert response.status_code == 422