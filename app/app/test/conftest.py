import json, os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.settings import db_session, SessionLocal
from app.main import app

json_file_path = os.path.join(os.path.dirname(__file__), "sample_data.json")
SAMPLE_DATA = json.load(open(json_file_path, 'r'))


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="function")
def client(test_db) -> Generator:
    def test_db_session():
        yield test_db
    app.dependency_overrides[db_session] = test_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides[db_session] = db_session


@pytest.fixture(scope="function")
def test_db() -> Generator:
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
