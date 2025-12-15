import uuid

def test_register_success(client):
    response = client.post(
        "/users/register",
        json={
            "username": f"user_{uuid.uuid4()}", # use uuid to test always with different usernames so it doesn't fails
            "email": f"{uuid.uuid4()}@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201
