from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.schemas.user import UserId


def all(db: Session, skip: int, limit: int):
    return db.query(Task).offset(skip).limit(limit).all()


def create(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def filterd_by_status(db: Session, statuses: list[int], skip: int, limit: int):
    return (
        db.query(Task)
        .filter(Task.status.in_(statuses))
        .order_by(desc(Task.status), desc(Task.priority), Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def not_assigned(db: Session, statuses: list[int], skip: int, limit: int):
    subquery = (
        ~db.query(Assignment.task_id).filter(Assignment.task_id == Task.id).exists()
    )
    return (
        db.query(Task)
        .filter(Task.status.in_(statuses))
        .filter(subquery)
        .order_by(desc(Task.priority), Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def not_resolved(
    db: Session, statuses: list[int], skip: int, limit: int, user_id: UserId
):
    return (
        db.query(Task)
        .join(Assignment)
        .filter(Task.status.in_(statuses))
        .filter(Assignment.user_id == user_id.id)
        .order_by(desc(Task.status), desc(Task.priority), Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
