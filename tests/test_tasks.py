 # security test that verifies logged user to acceed to the post functionality
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

def test_update_task(authorized_client):
    # first create a new task
    response = authorized_client.post(
        "/tasks/",
        json={"title": "Nueva tarea"},
    )

    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["id"]

    response_updated = authorized_client.put(
        f"/tasks/",
        json={
            "task_id": task_id,
            "title": "Tarea actualizada",
            "description": "descripcion de la tareita",
            "status": "in_progress",
        },
    )

    assert response_updated.status_code == 200

    updated_data = response_updated.json()

    assert updated_data["id"] == task_id
    assert updated_data["title"] == "Tarea actualizada"
    assert updated_data["status"] == "in_progress"

def test_delete_task(authorized_client):
    response = authorized_client.post(
        "/tasks/",
        json={"title": "Nueva tarea"},
    )

    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["id"]

    deleted = authorized_client.delete(
        f"/tasks/{task_id}",
    )

    assert deleted.status_code == 204


def test_delete_task_unexistent(authorized_client):
    task_id = 1234

    response = authorized_client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404

# helper for log out test
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
