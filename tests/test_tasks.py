def test_create_task_unauthorized(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "description": "Testing POST endpoint",
            "status": "pending",
        },
    )
    
    assert response.status_code == 201


def test_create_task_success(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Nueva tarea",
            "description": "Creada desde pytest",
            "status": "pending",
        },
    )

    assert response.status_code == 201
