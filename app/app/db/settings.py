from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_session():
    try:
        session_local = SessionLocal()
        yield session_local
    finally:
        session_local.close()