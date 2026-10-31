import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def clear_store():
    main._tasks.clear()
    yield
    main._tasks.clear()


def test_health_endpoints():
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/readyz").json() == {"status": "ready"}


def test_root_returns_version():
    body = client.get("/").json()
    assert body["service"] == "taskops-api"
    assert "version" in body


def test_task_crud_flow():
    created = client.post("/tasks", json={"title": "Write Dockerfile"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    assert client.get(f"/tasks/{task_id}").json()["title"] == "Write Dockerfile"
    assert len(client.get("/tasks").json()) == 1

    updated = client.put(f"/tasks/{task_id}", json={"title": "Write Dockerfile", "done": True})
    assert updated.json()["done"] is True

    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_invalid_task_rejected():
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_missing_task_returns_404():
    assert client.put("/tasks/nope", json={"title": "x"}).status_code == 404
    assert client.delete("/tasks/nope").status_code == 404


def test_metrics_exposed():
    client.get("/healthz")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "taskops_tasks" in response.text
