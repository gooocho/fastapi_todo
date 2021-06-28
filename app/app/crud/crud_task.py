from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskId, TaskUpdate
from app.schemas.user import UserId


def find(db: Session, task_id: TaskId):
    return db.query(Task).filter(Task.id == task_id.id).first()


def all(db: Session, limit: int, offset: int):
    return db.query(Task).limit(limit).offset(offset).all()


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


def update(db: Session, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task.id)
    compacted = {k: v for (k, v) in task.dict().items() if v is not None and k != "id"}
    if len(compacted):
        db_task.update(compacted)
        db.commit()
    return db_task.first()


def filterd_by_status(db: Session, statuses: List[int], limit: int, offset: int):
    return (
        db.query(Task)
        .filter(Task.status.in_(statuses))
        .order_by(desc(Task.status), desc(Task.priority), Task.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def not_assigned(db: Session, statuses: List[int], limit: int, offset: int):
    subquery = (
        ~db.query(Assignment.task_id).filter(Assignment.task_id == Task.id).exists()
    )
    return (
        db.query(Task)
        .filter(Task.status.in_(statuses))
        .filter(subquery)
        .order_by(desc(Task.priority), Task.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def not_resolved(
    db: Session, user_id: UserId, statuses: List[int], limit: int, offset: int
):
    return (
        db.query(Task)
        .join(Assignment)
        .filter(Task.status.in_(statuses))
        .filter(Assignment.user_id == user_id.id)
        .order_by(desc(Task.status), desc(Task.priority), Task.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
