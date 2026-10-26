
import os
import uuid

os.environ["DATABASE_URL"] = "sqlite:///./test_taskflow_v2.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-only-32bytes-minimum"

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_auth_and_crud():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    r = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )
    assert r.status_code == 201, r.text

    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/projects",
        json={"name": "Demo", "description": "Test"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    project_id = r.json()["id"]

    r = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "priority": "high",
            "status": "pending",
            "project_id": project_id,
        },
        headers=headers,
    )
    assert r.status_code == 201, r.text
    task_id = r.json()["id"]

    r = client.put(
        f"/tasks/{task_id}",
        json={"status": "completed"},
        headers=headers,
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "completed"

    r = client.get("/tasks", headers=headers)
    assert r.status_code == 200, r.text
    assert len(r.json()) == 1

    r = client.get(
        "/tasks/search",
        params={"title": "Write tests", "algo": "binary"},
        headers=headers,
    )
    assert r.status_code == 200, r.text

    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 200, r.text


def test_tasks_require_authentication():
    response = client.get("/tasks")

    assert response.status_code in (401, 403), response.text


def test_task_creation_rejects_missing_title():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Validation Test",
            "email": email,
            "password": "password123",
        },
    )
    assert response.status_code == 201, response.text

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/tasks",
        json={},
        headers=headers,
    )

    assert response.status_code == 422, response.text


def test_login_rejects_wrong_password():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Login Test",
            "email": email,
            "password": "password123",
        },
    )
    assert response.status_code == 201, response.text

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401, response.text


def test_user_cannot_access_another_users_task():
    # Register the owner.
    email1 = f"owner-{uuid.uuid4().hex[:8]}@example.com"
    r1 = client.post(
        "/auth/register",
        json={
            "name": "Owner",
            "email": email1,
            "password": "password123",
        },
    )
    assert r1.status_code == 201, r1.text
    headers1 = {"Authorization": f"Bearer {r1.json()['access_token']}"}

    # Create a project owned by the first user.
    project = client.post(
        "/projects",
        json={"name": "Private Project", "description": "Owner only"},
        headers=headers1,
    )
    assert project.status_code == 201, project.text

    # Create a task in that project.
    task = client.post(
        "/tasks",
        json={
            "title": "Private Task",
            "priority": "high",
            "status": "pending",
            "project_id": project.json()["id"],
        },
        headers=headers1,
    )
    assert task.status_code == 201, task.text
    task_id = task.json()["id"]

    # Register a different user.
    email2 = f"other-{uuid.uuid4().hex[:8]}@example.com"
    r2 = client.post(
        "/auth/register",
        json={
            "name": "Other User",
            "email": email2,
            "password": "password123",
        },
    )
    assert r2.status_code == 201, r2.text
    headers2 = {"Authorization": f"Bearer {r2.json()['access_token']}"}

    # The second user must not access the first user's task.
    response = client.get(f"/tasks/{task_id}", headers=headers2)
    assert response.status_code == 404, response.text
