from tests.test_tasks import get_auth_headers


def test_logout_revokes_token(client):
    headers = get_auth_headers(client)

    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Fail"},
    )

    assert response.status_code == 401
