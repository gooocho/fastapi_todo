from enum import IntEnum, unique
from typing import Optional

from pydantic import BaseModel, Field


@unique
class TaskPriority(IntEnum):
    """
    優先度

    数値が大きいと優先度が高い
    """

    LOW = 1
    BELOW_NORMAL = 2
    NORMAL = 3
    ABOVE_NORMAL = 4
    HIGH = 5


@unique
class TaskStatus(IntEnum):
    """
    ステータス

    1: 未着手
    2: 作業中
    3: 完了
    """

    NEW = 1
    IN_PROGRESS = 2
    RESOLVED = 3


NOT_RESOLVED = [TaskStatus.NEW, TaskStatus.IN_PROGRESS]


class TaskId(BaseModel):
    id: int


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    description: str
    priority: Optional[TaskPriority] = Field(TaskPriority.NORMAL)
    status: Optional[TaskStatus] = Field(TaskStatus.NEW)


class TaskUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    priority: Optional[TaskPriority]
    status: Optional[TaskStatus]


class Task(TaskBase):
    id: int
    description: str
    priority: int
    status: int

    class Config:
        orm_mode = True
