from enum import Enum, unique
from pydantic import BaseModel
from typing import Optional

class TaskCreateReq(BaseModel):
    title: str
    description: str
    priority: Optional[int] = None
    status: Optional[int] = None



@unique
class PriorityName(str, Enum):
    LOW = 1
    BELOW_NORMAL = 2
    NORMAL = 3
    ABOVE_NORMAL = 4
    HIGH = 5


@unique
class StatusName(str, Enum):
    NEW = 1
    IN_PROGRESS = 2
    RESOLVED = 3


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: int

    class Config:
        orm_mode = True
