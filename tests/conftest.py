import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

app.dependency_overrides[get_db] = override_get_db

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
def authorized_client(): 
    def override_get_current_user(): return User( id=1, email="test@test.com", is_active=True, ) 
    app.dependency_overrides[get_current_user] = override_get_current_user 
    client = TestClient(app) 
    yield client 
    app.dependency_overrides.clear()