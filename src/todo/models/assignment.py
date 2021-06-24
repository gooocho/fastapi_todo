from sqlalchemy import Column, ForeignKey, Integer

from ...repository.config import Base


class Assignment(Base):
    __tablename__ = "assignments"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
