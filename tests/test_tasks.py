def test_create_task_requires_auth(client):
    response = client.post(
        "/tasks/",
        json={"title": "Nueva tarea"},
    )

    assert response.status_code == 401

def test_create_task_success_with_auth(authorized_client):
    response = authorized_client.post(
        "/tasks/",
        json={"title": "Nueva tarea"},
    )

    assert response.status_code == 201



def get_auth_headers(client):
    client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "test@test.com",
            "password": "123456",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
