from fastapi import status
from fastapi.testclient import TestClient


class TestUserStatistics:
    def test_assigned_task_counts(self, client: TestClient) -> None:
        response = client.get("/user_statistics/assigned_task_counts?page=1&per_page=4")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"user_id": 1, "priority_task_counts": []},
            {
                "user_id": 2,
                "priority_task_counts": [
                    {"priority": 5, "task_count": 5},
                    {"priority": 4, "task_count": 4},
                    {"priority": 3, "task_count": 3},
                    {"priority": 2, "task_count": 2},
                    {"priority": 1, "task_count": 1},
                ],
            },
            {"user_id": 3, "priority_task_counts": []},
            {
                "user_id": 4,
                "priority_task_counts": [
                    {"priority": 5, "task_count": 6},
                    {"priority": 4, "task_count": 5},
                    {"priority": 3, "task_count": 4},
                    {"priority": 2, "task_count": 3},
                    {"priority": 1, "task_count": 2},
                ],
            },
        ]

    def test_resolved_task_counts(self, client: TestClient) -> None:
        response = client.get("/user_statistics/resolved_task_counts?page=1&per_page=3")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"user_id": 4, "task_count": 20},
            {"user_id": 3, "task_count": 15},
            {"user_id": 1, "task_count": 0},
        ]
