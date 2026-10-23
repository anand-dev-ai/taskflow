
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
