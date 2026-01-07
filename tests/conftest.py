import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import get_password_hash
from app.db.models.models import UserRole
from app.main import app
from app.db.base_class import Base
from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db

# my isolated db used only for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# create sessions only for the tests db
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# replace the real conection for the tests conection
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def override_db_dependency():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


# automatically teardown of the tests db for each test
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

#http client withouth auth
@pytest.fixture
def client():
    return TestClient(app)

# mock used to fake a logged user
@pytest.fixture
def authorized_client(client, test_user):
    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)



@pytest.fixture
def test_user(db):
    user = User(
        username=f"user_{uuid.uuid4()}",
        email=f"{uuid.uuid4()}@test.com",
        hashed_password="hashed",
        is_active=True,
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def admin_user():
    db = TestingSessionLocal()
    admin = db.query(User).filter(User.email == "admin@test.com").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@test.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    db.close()
    return admin

@pytest.fixture
def admin_client(client, admin_user):
    response = client.post(
        "/auth/login",
        data={
            "username": admin_user.email,
            "password": "admin123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    yield client

    client.headers.pop("Authorization", None)
