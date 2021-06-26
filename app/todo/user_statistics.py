from typing import List

from itertools import groupby

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_assignment, crud_user
from app.repository.config import repository_session
from app.schemas.task import TaskStatus
from app.schemas.user import User
from app.schemas.user_statistics import UserTaskCounts, TaskCount

user_statistics = APIRouter(prefix="/user_statistics")


@user_statistics.get(
    "/assigned_task_counts",
    response_model=List[UserTaskCounts],
    tags=["user_statistics"],
)
async def assigned_task_counts(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    """
    ユーザーにアサインされている作業中のタスクの数を優先度別に集計する
    １つも作業中のタスクを持たないユーザーも出現する
    """
    users = crud_user.all(db=db, skip=skip, limit=limit)

    assigned_task_counts = crud_assignment.assigned_task_counts(
        db=db, status=TaskStatus.IN_PROGRESS, user_ids=[user.id for user in users]
    )

    user_id_2_rows = {
        user_id: list(row)
        for user_id, row in groupby(assigned_task_counts, lambda row: row.user_id)
    }

    return [
        UserTaskCounts(
            user=user,
            task_counts=[
                TaskCount(priority=row.priority, count=row.task_count)
                for row in user_id_2_rows.get(user.id, [])
            ],
        )
        for user in users
    ]
