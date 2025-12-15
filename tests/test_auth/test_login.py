def test_login_success(client):
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

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_access_protected_endpoint(client):
    client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "123456",
        },
    )

    login = client.post(
    "/auth/login",
    data={
        "username": "test@test.com",
        "password": "123456",
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

    print("LOGIN RESPONSE:", login.json())
    token = login.json()["access_token"]


    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Task protegida",
            "description": "Con token",
            "status": "pending",
        },
    )

    assert response.status_code == 201

def test_login_wrong_password(client):
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
            "password": "WRONG",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
