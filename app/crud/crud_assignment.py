from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.task import Task
from app.models.user import User


def assign(db: Session, user_id: int, task_id: int):
    db_user = db.query(User).get(user_id)
    db_task = db.query(Task).get(task_id)
    db_user.tasks.append(db_task)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return [db_user, db_task]


def assigned_task_counts(
    db: Session, user_ids: list[int], status: int
):
    return (
        db.query(
            Assignment.user_id,
            Task.priority,
            func.count(Task.id).label("task_count"),
        )
        .join(Task)
        .filter(Assignment.user_id.in_(user_ids))
        .filter(Task.status == status)
        .group_by(Assignment.user_id, Task.priority)
        .order_by(Assignment.user_id, desc(Task.priority))
        .all()
    )
