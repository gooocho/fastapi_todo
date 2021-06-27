from itertools import groupby
from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_user, crud_user_statistics
from app.repository.config import repository_session
from app.schemas.task import TaskStatus
from app.schemas.user import UserId
from app.schemas.user_statistics import PriorityTaskCount, PriorityTaskCounts, TaskCount

user_statistics = APIRouter(prefix="/user_statistics")


@user_statistics.get(
    "/assigned_task_counts",
    response_model=List[PriorityTaskCounts],
    tags=["user_statistics"],
)
async def assigned_task_counts(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    """
    ユーザーにアサインされている作業中のタスクの数を優先度別に集計する
    １つも作業中のタスクを持たないユーザーも出現する
    """
    user_ids: List[UserId] = crud_user.all_id(db=db, skip=skip, limit=limit)

    assigned_task_counts = crud_user_statistics.assigned_task_counts(
        db=db, user_ids=user_ids, status=TaskStatus.IN_PROGRESS
    )

    user_id_2_assigned_task_counts = {
        user_id: list(row)
        for user_id, row in groupby(assigned_task_counts, lambda row: row.user_id)
    }

    return [
        PriorityTaskCounts(
            user_id=user_id.id,
            priority_task_counts=[
                PriorityTaskCount(priority=row.priority, task_count=row.task_count)
                for row in user_id_2_assigned_task_counts.get(user_id.id, [])
            ],
        )
        for user_id in user_ids
    ]


@user_statistics.get(
    "/resolved_task_counts",
    response_model=List[TaskCount],
    tags=["user_statistics"],
)
async def resolved_task_counts(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    """
    ユーザーが完了させたタスクの数を集計する
    完了させたタスクの数(多->少), ID(低->高)の順で出力される
    １つもタスクを完了させていないユーザーも出現する
    """
    rows = crud_user_statistics.status_task_counts(
        db=db, status=TaskStatus.RESOLVED, skip=skip, limit=limit
    )
    return [TaskCount(user_id=row.id, task_count=row.task_count) for row in rows]
