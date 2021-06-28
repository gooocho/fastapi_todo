from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:postgres@fastapi_todo_db:5432/fastapi_todo"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def postgres_db_session():
    try:
        session_local = SessionLocal()
        yield session_local
    finally:
        session_local.close()
