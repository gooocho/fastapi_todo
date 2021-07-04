from fastapi import status
from fastapi.testclient import TestClient


class TestUsers:
    def test_list_users(self, client: TestClient) -> None:
        response = client.get("/users/list?page=1&per_page=2")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"id": 1, "name": "user1", "mail": "user1@example.com"},
            {"id": 2, "name": "user2", "mail": "user2@example.com"},
        ]

    def test_get_user(self, client: TestClient) -> None:
        response = client.get("/users/get/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "user1",
            "mail": "user1@example.com",
        }

    def test_create_user(self, client: TestClient) -> None:
        task_counts = len(client.get("/users/list?page=1&per_page=10").json())
        response = client.post(
            "/users/create",
            json={"name": "user7", "mail": "user7@example.com"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": 7,
            "name": "user7",
            "mail": "user7@example.com",
        }
        assert (
            len(client.get("/users/list?page=1&per_page=10").json()) == task_counts + 1
        )

    def test_update_user(self, client: TestClient) -> None:
        response1 = client.put(
            "/users/update",
            json={
                "id": 1,
                "name": "user1_updated",
                "mail": "user1_updated@example.com",
            },
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json() == {
            "id": 1,
            "name": "user1_updated",
            "mail": "user1_updated@example.com",
        }
        response2 = client.get("/users/get/1")
        assert response2.json() == {
            "id": 1,
            "name": "user1_updated",
            "mail": "user1_updated@example.com",
        }

    def test_delete_user(self, client: TestClient) -> None:
        response1 = client.delete(
            "/users/delete/1",
        )
        assert response1.status_code == status.HTTP_204_NO_CONTENT
        assert response1.json() == None
        response2 = client.get("/users/get/1")
        assert response2.status_code == status.HTTP_404_NOT_FOUND

    def test_not_resolved_tasks(self, client: TestClient) -> None:
        response = client.get("/users/2/tasks/not_resolved?page=1&per_page=3")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"id": 35, "title": "35", "description": "", "priority": 5, "status": 2},
            {"id": 36, "title": "36", "description": "", "priority": 5, "status": 2},
            {"id": 37, "title": "37", "description": "", "priority": 5, "status": 2},
        ]
