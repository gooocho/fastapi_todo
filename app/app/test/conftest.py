from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.settings import SessionLocal
from app.main import app


SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "user1", "mail": "user1@example.com"},
        {"id": 2, "name": "user2", "mail": "user2@example.com"},
        {"id": 3, "name": "user3", "mail": "user3@example.com"},
        {"id": 4, "name": "user4", "mail": "user4@example.com"},
        {"id": 5, "name": "user5", "mail": "user5@example.com"},
        {"id": 6, "name": "user6", "mail": "user6@example.com"},
    ],
    "tasks": [
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
        {
            "id": 4,
            "title": "task4 title",
            "description": "task4 description",
            "priority": 1,
            "status": 1,
        },
        {
            "id": 5,
            "title": "task5 title",
            "description": "task5 description",
            "priority": 1,
            "status": 1,
        },
        {
            "id": 6,
            "title": "task6 title",
            "description": "task6 description",
            "priority": 1,
            "status": 1,
        },
    ],
    "assignments": [
        {"user_id": 2, "task_id": 1},
        {"user_id": 2, "task_id": 2},
        {"user_id": 2, "task_id": 3},
        {"user_id": 3, "task_id": 4},
        {"user_id": 4, "task_id": 1},
        {"user_id": 4, "task_id": 2},
        {"user_id": 4, "task_id": 3},
        {"user_id": 4, "task_id": 4},
        {"user_id": 4, "task_id": 5},
        {"user_id": 4, "task_id": 6},
        {"user_id": 5, "task_id": 1},
        {"user_id": 5, "task_id": 2},
        {"user_id": 5, "task_id": 3},
        {"user_id": 6, "task_id": 2},
        {"user_id": 6, "task_id": 4},
    ],
}


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def sample_db() -> Generator:
    db = SessionLocal()

    db.execute(f"TRUNCATE users CASCADE;")
    db.execute(f"TRUNCATE tasks CASCADE;")
    db.execute(f"TRUNCATE assignments CASCADE;")
    db.execute(f"SELECT setval('users_id_seq', 1, false);")
    db.execute(f"SELECT setval('tasks_id_seq', 1, false);")

    users_values = ",".join(
        [
            f"('{data_dict['name']}', '{data_dict['mail']}')"
            for data_dict in SAMPLE_DATA["users"]
        ]
    )
    tasks_values = ",".join(
        [
            f"('{data_dict['title']}', '{data_dict['description']}', {data_dict['priority']}, {data_dict['status']})"
            for data_dict in SAMPLE_DATA["tasks"]
        ]
    )
    db.execute(f"INSERT INTO users(name, mail) VALUES {users_values};")
    db.execute(
        f"INSERT INTO tasks(title, description, priority, status) VALUES {tasks_values};"
    )
    assignments_values = ",".join(
        [
            f"('{data_dict['user_id']}', '{data_dict['task_id']}')"
            for data_dict in SAMPLE_DATA["assignments"]
        ]
    )
    db.execute(
        f"INSERT INTO assignments(user_id, task_id) VALUES {assignments_values};"
    )
    yield db
    db.rollback()
