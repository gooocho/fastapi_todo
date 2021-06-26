from pydantic import BaseModel

from app.schemas.user import User


class TaskCount(BaseModel):
    priority: int
    count: int


class UserTaskCounts(BaseModel):
    user: User
    task_counts: list[TaskCount]
