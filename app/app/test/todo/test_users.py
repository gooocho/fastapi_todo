from fastapi import status
from fastapi.testclient import TestClient


def test_list_users(client: TestClient) -> None:
    response = client.get("/users/list?page=1&per_page=2")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "user1", "mail": "user1@example.com"},
        {"id": 2, "name": "user2", "mail": "user2@example.com"},
    ]


def test_get_user(client: TestClient) -> None:
    response = client.get("/users/get/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "user1", "mail": "user1@example.com"}


def test_create_user(client: TestClient) -> None:
    task_counts = len(client.get("/users/list?page=1&per_page=10").json())
    response = client.post(
        "/users/create",
        json={"name": "user7", "mail": "user7@example.com"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 7, "name": "user7", "mail": "user7@example.com"}
    assert len(client.get("/users/list?page=1&per_page=10").json()) == task_counts + 1


def test_update_user(client: TestClient) -> None:
    response1 = client.put(
        "/users/update",
        json={"id": 1, "name": "user1_updated", "mail": "user1_updated@example.com"},
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


def test_delete_user(client: TestClient) -> None:
    response1 = client.delete(
        "/users/delete/1",
    )
    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response1.json() == None
    response2 = client.get("/users/get/1")
    assert response2.status_code == status.HTTP_404_NOT_FOUND


def test_not_resolved_tasks(client: TestClient) -> None:
    response = client.get("/users/2/tasks/not_resolved?page=1&per_page=10")
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
        {
            "title": "task3 title",
            "id": 3,
            "description": "task3 description",
            "priority": 1,
            "status": 1,
        },
    ]
