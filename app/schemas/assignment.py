from pydantic import BaseModel

from app.schemas.task import Task
from app.schemas.user import User


class AssignmentBase(BaseModel):
    user_id: int
    task_id: int


class UserTaskPair(BaseModel):
    user: User
    task: Task


class Assignment(AssignmentBase):
    class Config:
        orm_mode = True
