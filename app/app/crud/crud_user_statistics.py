from typing import List

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from app.models.assignment import Assignment
from app.models.task import Task
from app.models.user import User
from app.schemas.user import UserId


def assigned_task_counts(db: Session, user_ids: List[UserId], status: int):
    return (
        db.query(
            Assignment.user_id,
            Task.priority,
            func.count(Task.id).label("task_count"),
        )
        .join(Task)
        .filter(Assignment.user_id.in_([user_id.id for user_id in user_ids]))
        .filter(Task.status == status)
        .group_by(Assignment.user_id, Task.priority)
        .order_by(Assignment.user_id, desc(Task.priority))
        .all()
    )


def status_task_counts(db: Session, status: int, limit: int, offset: int):
    subquery = (
        db.query(Assignment.user_id, func.count(Task.id).label("task_count"))
        .join(Task)
        .filter(Task.status == status)
        .group_by(Assignment.user_id)
        .subquery()
    )
    return (
        db.query(User.id, coalesce(subquery.c.task_count, 0).label("task_count"))
        .outerjoin(subquery)
        .order_by(desc(coalesce(subquery.c.task_count, 0)), User.id)
        .limit(limit)
        .offset(offset)
        .all()
    )