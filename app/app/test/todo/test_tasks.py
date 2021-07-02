from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.task import TaskPriority, TaskStatus


def test_list_tasks(client: TestClient) -> None:
    response = client.get("/tasks/list?page=1&per_page=2")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "task1 title",
            "id": 1,
            "description": "task1 description",
            "priority": 1,
            "status": 1,
        },
        {
            "title": "task2 title",
            "id": 2,
            "description": "task2 description",
            "priority": 1,
            "status": 1,
        },
    ]


def test_get_task(client: TestClient) -> None:
    response = client.get("/tasks/get/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "task1 title",
        "id": 1,
        "description": "task1 description",
        "priority": 1,
        "status": 1,
    }


def test_create_task(client: TestClient) -> None:
    task_counts = len(client.get("/tasks/list?page=1&per_page=10").json())
    response = client.post(
        "/tasks/create",
        json={
            "title": "task7 title updated",
            "description": "task7 description updated",
            "priority": TaskPriority.NORMAL,
            "status": TaskStatus.NEW,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "title": "task7 title updated",
        "id": 7,
        "description": "task7 description updated",
        "priority": 3,
        "status": 1,
    }
    assert len(client.get("/tasks/list?page=1&per_page=10").json()) == task_counts + 1


def test_update_task(client: TestClient) -> None:
    response = client.put(
        "/tasks/update",
        json={
            "id": 1,
            "title": "task1 title updated",
            "description": "task1 description updated",
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.RESOLVED,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "task1 title updated",
        "description": "task1 description updated",
        "priority": 5,
        "status": 3,
    }


def test_not_resolved_tasks(client: TestClient) -> None:
    response = client.get("/tasks/not_resolved?page=1&per_page=3")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "task1 title",
            "description": "task1 description",
            "priority": 1,
            "status": 1,
        },
        {
            "id": 2,
            "title": "task2 title",
            "description": "task2 description",
            "priority": 1,
            "status": 1,
        },
        {
            "id": 3,
            "title": "task3 title",
            "description": "task3 description",
            "priority": 1,
            "status": 1,
        },
    ]


def test_not_assigned_tasks(client: TestClient) -> None:
    response = client.get("/tasks/not_assigned?page=1&per_page=3")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
