from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.repository.config import Base
from app.models.assignment import Assignment


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    status = Column(Integer, index=True)

    users = relationship(
        "User",
        secondary=Assignment.__tablename__,
        back_populates="tasks",
    )
