import json, os, pytest

from typing import Generator

from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.db.settings import Base, db_session, SessionLocal
from app.main import app

SQLALCHEMY_TEST_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_SERVER"),
    port=os.getenv("POSTGRES_PORT"),
    path=f"/{os.getenv('POSTGRES_DB')}_test",
)
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URI, pool_pre_ping=True, echo=True)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


json_file_path = os.path.join(os.path.dirname(__file__), "sample_data.json")
SAMPLE_DATA = json.load(open(json_file_path, "r"))
users_values_clause = ",".join(
    [
        f"('{data_dict['name']}', '{data_dict['mail']}')"
        for data_dict in SAMPLE_DATA["users"]
    ]
)
tasks_values_clause = ",".join(
    [
        f"('{data_dict['title']}', '{data_dict['description']}', {data_dict['priority']}, {data_dict['status']})"
        for data_dict in SAMPLE_DATA["tasks"]
    ]
)
assignments_values_clause = ",".join(
    [
        f"('{data_dict['user_id']}', '{data_dict['task_id']}')"
        for data_dict in SAMPLE_DATA["assignments"]
    ]
)


@pytest.fixture(scope="function")
def new_test_db() -> Generator:
    test_db_url = str(SQLALCHEMY_TEST_DATABASE_URI)
    try:
        assert not database_exists(test_db_url)
        create_database(test_db_url)
        Base.metadata.create_all(bind=test_engine)
        app.dependency_overrides[db_session] = test_db
        yield
        app.dependency_overrides[db_session] = db_session
    finally:
        drop_database(test_db_url)


@pytest.fixture(scope="function")
def test_db(new_test_db):
    try:
        session_local = TestSessionLocal()
        session_local.execute(
            f"INSERT INTO users(name, mail) VALUES {users_values_clause};"
        )
        session_local.execute(
            f"INSERT INTO tasks(title, description, priority, status) VALUES {tasks_values_clause};"
        )
        session_local.execute(
            f"INSERT INTO assignments(user_id, task_id) VALUES {assignments_values_clause};"
        )
        yield session_local
    finally:
        session_local.close()


@pytest.fixture(scope="function")
def client(new_test_db) -> Generator:
    def test_db_session():
        yield new_test_db

    app.dependency_overrides[db_session] = test_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides[db_session] = db_session
