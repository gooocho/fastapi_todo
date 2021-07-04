import pytest

from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.task import TaskPriority, TaskStatus


class TestTasks:
    @pytest.mark.parametrize(
        "page, per_page, expect",
        [
            (
                1,
                2,
                [
                    {
                        "id": 1,
                        "title": "1",
                        "description": "",
                        "priority": 1,
                        "status": 1,
                    },
                    {
                        "id": 2,
                        "title": "2",
                        "description": "",
                        "priority": 1,
                        "status": 1,
                    },
                ],
            ),
            (
                2,
                2,
                [
                    {
                        "id": 3,
                        "title": "3",
                        "description": "",
                        "priority": 2,
                        "status": 1,
                    },
                    {
                        "id": 4,
                        "title": "4",
                        "description": "",
                        "priority": 2,
                        "status": 1,
                    },
                ],
            ),
            (
                1,
                3,
                [
                    {
                        "id": 1,
                        "title": "1",
                        "description": "",
                        "priority": 1,
                        "status": 1,
                    },
                    {
                        "id": 2,
                        "title": "2",
                        "description": "",
                        "priority": 1,
                        "status": 1,
                    },
                    {
                        "id": 3,
                        "title": "3",
                        "description": "",
                        "priority": 2,
                        "status": 1,
                    },
                ],
            ),
        ],
    )
    def test_list_tasks(self, page, per_page, expect, client: TestClient) -> None:
        response = client.get(f"/tasks/list?page={page}&per_page={per_page}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expect

    def test_get_task(self, client: TestClient) -> None:
        response = client.get("/tasks/get/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "title": "1",
            "description": "",
            "priority": 1,
            "status": 1,
        }

    def test_create_task(self, client: TestClient) -> None:
        response = client.post(
            "/tasks/create",
            json={
                "title": "71",
                "description": "",
                "priority": TaskPriority.NORMAL,
                "status": TaskStatus.NEW,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": 71,
            "title": "71",
            "description": "",
            "priority": 3,
            "status": 1,
        }

    def test_update_task(self, client: TestClient) -> None:
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

    def test_not_resolved_tasks(self, client: TestClient) -> None:
        response = client.get("/tasks/not_resolved?page=1&per_page=3")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"title": "35", "id": 35, "description": "", "priority": 5, "status": 2},
            {"title": "36", "id": 36, "description": "", "priority": 5, "status": 2},
            {"title": "37", "id": 37, "description": "", "priority": 5, "status": 2},
        ]

    def test_not_assigned_tasks(self, client: TestClient) -> None:
        response = client.get("/tasks/not_assigned?page=1&per_page=3")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"id": 61, "title": "61", "description": "", "priority": 1, "status": 1},
            {"id": 62, "title": "62", "description": "", "priority": 1, "status": 1},
            {"id": 63, "title": "63", "description": "", "priority": 1, "status": 1},
        ]
