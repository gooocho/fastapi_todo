from fastapi import status
from fastapi.testclient import TestClient

class TestAssignments:
    def test_create_assignment(self, client: TestClient) -> None:
        response = client.post(
            "/assignments/create",
            json={"user_id": 5, "task_id": 1},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"user_id": 5, "task_id": 1}
