from fastapi import status
from fastapi.testclient import TestClient


def test_assigned_task_counts(client: TestClient) -> None:
    response = client.get("/user_statistics/assigned_task_counts?page=1&per_page=3")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"user_id": 1, "priority_task_counts": []},
        {"user_id": 2, "priority_task_counts": []},
        {"user_id": 3, "priority_task_counts": []},
    ]


def test_resolved_task_counts(client: TestClient) -> None:
    response = client.get("/user_statistics/resolved_task_counts?page=1&per_page=3")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"user_id": 1, "task_count": 0},
        {"user_id": 2, "task_count": 0},
        {"user_id": 3, "task_count": 0},
    ]
