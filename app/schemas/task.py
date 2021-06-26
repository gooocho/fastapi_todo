from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel


@unique
class TaskPriority(str, Enum):
    """
    優先度

    数値が大きい＝優先度が高い
    """
    LOW = 1
    BELOW_NORMAL = 2
    NORMAL = 3
    ABOVE_NORMAL = 4
    HIGH = 5


@unique
class TaskStatus(str, Enum):
    """
    ステータス

    NEW: 未着手
    IN_PROGRESS: 作業中
    RESOLVED: 完了
    """
    NEW = 1
    IN_PROGRESS = 2
    RESOLVED = 3


NOT_RESOLVED = [TaskStatus.NEW, TaskStatus.IN_PROGRESS]


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    description: str
    priority: Optional[int] = TaskPriority.NORMAL
    status: Optional[int] = TaskStatus.NEW


class Task(TaskBase):
    id: int
    description: str
    priority: int
    status: int

    class Config:
        orm_mode = True
