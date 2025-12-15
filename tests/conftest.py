import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user  
from app.db.models import User 

@pytest.fixture
def authorized_client():
    def override_get_current_user():
        return User(
            id=1,
            email="test@test.com",
            is_active=True,
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)
