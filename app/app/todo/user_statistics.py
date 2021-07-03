from itertools import groupby
from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_user, crud_user_statistics
from app.db.settings import db_session
from app.schemas.pager import Pager
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
    pager: Pager = Depends(), db: Session = Depends(db_session)
):
    """
    ユーザーにアサインされている作業中のタスクの数を優先度別に集計する。
    １つも作業中のタスクを持たないユーザーも出現する。
    """
    user_ids: List[UserId] = crud_user.all_id(
        db=db, limit=pager.per_page, offset=pager.offset()
    )

    model_assigned_task_counts = crud_user_statistics.assigned_task_counts(
        db=db, user_ids=user_ids, status=TaskStatus.IN_PROGRESS
    )

    user_id_2_model_assigned_task_counts = {
        user_id: list(row)
        for user_id, row in groupby(model_assigned_task_counts, lambda row: row.user_id)
    }

    return [
        PriorityTaskCounts(
            user_id=user_id.id,
            priority_task_counts=[
                PriorityTaskCount(
                    priority=model_assigned_task_count.priority,
                    task_count=model_assigned_task_count.task_count,
                )
                for model_assigned_task_count in user_id_2_model_assigned_task_counts.get(
                    user_id.id, []
                )
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
    pager: Pager = Depends(), db: Session = Depends(db_session)
):
    """
    ユーザーが完了させたタスクの数を集計する。
    1. 完了させたタスクの数が多いもの
    2. ID が小さいもの
    の順で出力される。
    １つもタスクを完了させていないユーザーも出現する。
    """
    model_status_task_counts = crud_user_statistics.status_task_counts(
        db=db,
        status=TaskStatus.RESOLVED,
        limit=pager.per_page,
        offset=pager.offset(),
    )
    return [
        TaskCount(
            user_id=model_status_task_count.id,
            task_count=model_status_task_count.task_count,
        )
        for model_status_task_count in model_status_task_counts
    ]
