from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.settings import Base
from app.models.assignment import ModelAssignment


class ModelTask(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    status = Column(Integer, index=True)

    users = relationship(
        "ModelUser",
        secondary=ModelAssignment.__tablename__,
        order_by="ModelUser.id",
        back_populates="tasks",
    )
