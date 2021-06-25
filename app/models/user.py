from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.repository.config import Base
from app.models.assignment import Assignment


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mail = Column(String, unique=True, index=True)

    tasks = relationship(
        "Task",
        secondary=Assignment.__tablename__,
        order_by="Task.id",
        back_populates="users",
    )
