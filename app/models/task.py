from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.assignment import Assignment
from app.repository.config import Base


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
        order_by="User.id",
        back_populates="tasks",
    )
