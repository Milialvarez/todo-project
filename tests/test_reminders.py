def test_create_reminder_requires_auth(client):
    response = client.post(
        "/reminders/",
        json={"date": "2025-12-31",
              "description": "happy new year's eve!!"},
    )

    assert response.status_code == 401

def test_create_reminder_success(authorized_client):
    response = authorized_client.post(
        "/reminders/",
        json={"date": "2025-12-31",
              "description": "happy new year's eve!!"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["description"] =="happy new year's eve!!"

def test_delete_reminder(authorized_client):
    response = authorized_client.post(
        "/reminders/",
        json={"date": "2025-12-31",
              "description": "happy new year's eve!!"},
    )

    reminder = response.json()
    reminder_id = reminder["id"]

    deletedReminder = authorized_client.delete(
        f"/reminders/{reminder_id}"
    )

    assert deletedReminder.status_code == 204

def test_update_reminder(authorized_client):
    response = authorized_client.post(
        "/reminders/",
        json={"date": "2025-12-31",
              "description": "happy new year's eve!!"},
    )

    reminder = response.json()
    reminder_id = reminder["id"]

    response_updated = authorized_client.put(
        f"/reminders/",
        json={
            "reminder_id": reminder_id,
            "date": "2026-01-01",
            "description": "officially happy new year!!",
        },
    )

    print(response_updated.json())

    data = response_updated.json()
    assert data["description"] == "officially happy new year!!"
    assert data["date"] =="2026-01-01"

def test_update_empty_reminder(authorized_client):
    response = authorized_client.post(
        "/reminders/",
        json={"date": "2025-12-31",
              "description": "happy new year's eve!!"},
    )

    reminder = response.json()
    reminder_id = reminder["id"]

    response_updated = authorized_client.put(
        f"/reminders/",
        json={
            "reminder_id": reminder_id,
            "date": None
        },
    )

    assert response_updated.status_code == 400

