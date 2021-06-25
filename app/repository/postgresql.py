from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:69f27de1009b478d8198b0249a2b7a62@localhost:5432/fastapi_todo"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def postgres_db_session():
    try:
        session_local = SessionLocal()
        yield session_local
    finally:
        session_local.close()
