from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.settings import Base
from app.models.assignment import ModelAssignment


class ModelUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mail = Column(String, unique=True, index=True)

    tasks = relationship(
        "ModelTask",
        secondary=ModelAssignment.__tablename__,
        order_by="ModelTask.id",
        back_populates="users",
    )
