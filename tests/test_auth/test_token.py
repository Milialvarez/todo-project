from app.db.models.models import User


def test_invalid_access_token(client):
    response = client.post(
        "/tasks/",
        headers={"Authorization": "Bearer invalidtoken"},
        json={"title": "no"},
    )
    assert response.status_code == 401

def test_refresh_token_success(client):
    client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "123456",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "test@test.com",
            "password": "123456",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200

    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_fails_if_user_deactivated_by_admin(client, admin_client, db):
    register_response = client.post(
        "/users/register",
        json={
            "username": "mili",
            "email": "mili@test.com",
            "password": "123456",
        },
    )

    assert register_response.status_code == 201
    user_data = register_response.json()
    user_id = user_data["id"]

    login = client.post(
        "/auth/login",
        data={
            "username": "mili@test.com",
            "password": "123456",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login.status_code == 200
    tokens = login.json()
    refresh_token = tokens["refresh_token"]

    response = admin_client.patch(
        f"/admin/users/{user_id}/toggle-active"
    )
    assert response.status_code == 200

    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert refresh_response.status_code == 403

def test_get_all_users(client, admin_client, db):
    register_response = client.post(
        "/users/register",
        json={
            "username": "normal user",
            "email": "testemail@test.com",
            "password": "123456",
        },
    )

    assert register_response.status_code == 201

    response = admin_client.get("/admin/users")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1

    usernames = [user["username"] for user in users]
    assert "mili" in usernames

def test_get_only_active_users(admin_client):
    response = admin_client.get("/admin/users?is_active=true")

    assert response.status_code == 200
    users = response.json()

    assert all(user["is_active"] is True for user in users)

def test_non_admin_cannot_get_users(authorized_client):
    response = authorized_client.get("/admin/users")
    assert response.status_code == 403

def test_change_roles(admin_client, client, db):
    register_response = client.post(
        "/users/register",
        json={
            "username": "user with normal role",
            "email": "usertest@gmail.com",
            "password": "123456",
        },
    )

    assert register_response.status_code == 201
    user_data = register_response.json()
    user_id = user_data["id"]

    response = admin_client.patch(
        f"/admin/users/{user_id}/toggle-role"
    )

    assert response.status_code == 200

    user_updated = response.json()
    assert user_updated["role"] == "admin"




    
