from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user(client: TestClient, db: Session) -> None:
    data = {"name": "user1", "mail": "user1@example.com"}
    response = client.post(
        f"/users/create",
        json=data,
    )
    assert response.status_code == 200
