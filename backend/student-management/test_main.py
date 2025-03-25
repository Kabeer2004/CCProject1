import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Student  # Import models explicitly

# Setup test database
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal

# Dependency override
@pytest.fixture(scope="module")
def override_get_db(test_db):
    def _override_get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()
    return _override_get_db

@pytest.fixture(scope="module")
def client(override_get_db):
    # Apply dependency override
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()

def test_create_and_get_student(client):
    # First create a test user
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpass"}
    )
    assert user_response.status_code == 200
    
    # Get token
    token_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = token_response.json()["access_token"]
    
    # Test creating student with auth
    student_data = {
        "name": "Test Student",
        "age": 20,
        "email": "test@example.com"
    }
    
    create_response = client.post(
        "/students/",
        json=student_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 201
    
    # Get student
    student_id = create_response.json()["id"]
    get_response = client.get(
        f"/students/{student_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Student"