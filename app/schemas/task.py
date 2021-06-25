from enum import Enum, unique
from pydantic import BaseModel
from typing import Optional

@unique
class Priority(str, Enum):
    LOW = 1
    BELOW_NORMAL = 2
    NORMAL = 3
    ABOVE_NORMAL = 4
    HIGH = 5


@unique
class Status(str, Enum):
    NEW = 1
    IN_PROGRESS = 2
    RESOLVED = 3


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    description: str
    priority: Optional[int] = Priority.NORMAL
    status: Optional[int] = Status.NEW


class Task(TaskBase):
    id: int
    description: str
    priority: int
    status: int

    class Config:
        orm_mode = True
