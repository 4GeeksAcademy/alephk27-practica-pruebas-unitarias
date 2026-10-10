import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def task_store():
    missing = object()
    original_tasks = getattr(app.state, "tasks", missing)
    yield app.state

    if original_tasks is missing:
        if hasattr(app.state, "tasks"):
            del app.state.tasks
    else:
        app.state.tasks = original_tasks


@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def test_get_tasks_returns_all_registered_tasks(client, task_store):
    expected_tasks = [
        {"id": 1, "title": "Preparar entrega", "completed": False},
        {"id": 2, "title": "Revisar pruebas", "completed": True},
    ]
    task_store.tasks = expected_tasks

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == expected_tasks


def test_get_tasks_returns_empty_list_when_no_tasks_exist(client, task_store):
    task_store.tasks = []

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_does_not_expose_details_when_storage_fails(client, task_store):
    class BrokenTaskStore(list):
        def __iter__(self):
            raise RuntimeError("internal storage credentials")

    task_store.tasks = BrokenTaskStore()

    response = client.get("/tasks")

    assert response.status_code == 500
    assert "credentials" not in response.text