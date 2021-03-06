from typing import List

from pydantic import BaseModel


class PriorityTaskCount(BaseModel):
    priority: int
    task_count: int


class PriorityTaskCounts(BaseModel):
    user_id: int
    priority_task_counts: List[PriorityTaskCount]


class TaskCount(BaseModel):
    user_id: int
    task_count: int
