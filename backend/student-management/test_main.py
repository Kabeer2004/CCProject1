# test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Student, Course, Enrollment  # Updated imports

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
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_and_get_student(client):
    user_response = client.post("/users/", json={"username": "testuser", "password": "testpass"})
    assert user_response.status_code == 200
    token_response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = token_response.json()["access_token"]
    student_data = {"name": "Test Student", "age": 20, "email": "test@example.com"}
    create_response = client.post("/students/", json=student_data, headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == 201
    student_id = create_response.json()["id"]
    get_response = client.get(f"/students/{student_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Student"

# New tests
def test_course_and_enrollment_flow(client):
    # Create user and get token
    client.post("/users/", json={"username": "testuser2", "password": "testpass"})
    token_response = client.post("/token", data={"username": "testuser2", "password": "testpass"})
    token = token_response.json()["access_token"]

    # Create a course
    course_data = {"title": "Mathematics", "description": "Introduction to Mathematics"}
    create_course_response = client.post("/courses/", json=course_data, headers={"Authorization": f"Bearer {token}"})
    assert create_course_response.status_code == 201
    course_id = create_course_response.json()["id"]
    assert create_course_response.json()["title"] == "Mathematics"

    # Get the course
    get_course_response = client.get(f"/courses/{course_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_course_response.status_code == 200
    assert get_course_response.json()["description"] == "Introduction to Mathematics"

    # Create a student
    student_data = {"name": "Jane Doe", "age": 20, "email": "jane@example.com"}
    create_student_response = client.post("/students/", json=student_data, headers={"Authorization": f"Bearer {token}"})
    assert create_student_response.status_code == 201
    student_id = create_student_response.json()["id"]

    # Enroll student in course
    enrollment_data = {"student_id": student_id, "course_id": course_id}
    enroll_response = client.post("/enrollments", json=enrollment_data, headers={"Authorization": f"Bearer {token}"})
    assert enroll_response.status_code == 200
    assert enroll_response.json() == {"message": "Enrollment successful"}

    # Get student's enrolled courses
    get_enrolled_response = client.get(f"/students/{student_id}/courses/", headers={"Authorization": f"Bearer {token}"})
    assert get_enrolled_response.status_code == 200
    assert get_enrolled_response.json() == {"enrolled_courses": [course_id]}

def test_enrollment_errors(client):
    # Create user and get token
    client.post("/users/", json={"username": "testuser3", "password": "testpass"})
    token_response = client.post("/token", data={"username": "testuser3", "password": "testpass"})
    token = token_response.json()["access_token"]

    # Create a course and student
    course_response = client.post("/courses/", json={"title": "Physics", "description": "Intro to Physics"}, headers={"Authorization": f"Bearer {token}"})
    course_id = course_response.json()["id"]
    student_response = client.post("/students/", json={"name": "John", "age": 21, "email": "john@example.com"}, headers={"Authorization": f"Bearer {token}"})
    student_id = student_response.json()["id"]

    # Enroll student
    client.post("/enrollments", json={"student_id": student_id, "course_id": course_id}, headers={"Authorization": f"Bearer {token}"})

    # Try enrolling non-existent student
    response = client.post("/enrollments", json={"student_id": 999, "course_id": course_id}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

    # Try enrolling in non-existent course
    response = client.post("/enrollments", json={"student_id": student_id, "course_id": 999}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

    # Try enrolling again (duplicate)
    response = client.post("/enrollments", json={"student_id": student_id, "course_id": course_id}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Already enrolled"