from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.assignment import ModelAssignment
from app.models.task import ModelTask
from app.schemas.task import TaskCreate, TaskId, TaskStatus, TaskUpdate
from app.schemas.user import UserId


def find(db: Session, task_id: TaskId):
    return db.query(ModelTask).filter(ModelTask.id == task_id.id).first()


def all(db: Session, limit: int, offset: int):
    return db.query(ModelTask).order_by(ModelTask.id).limit(limit).offset(offset).all()


def create(db: Session, task: TaskCreate):
    db_task = ModelTask(
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
    db_task = db.query(ModelTask).filter(ModelTask.id == task.id)
    compacted = {k: v for (k, v) in task.dict().items() if v is not None and k != "id"}
    if len(compacted):
        db_task.update(compacted)
        db.commit()
    return db_task.first()


def filterd_by_status(db: Session, statuses: List[TaskStatus], limit: int, offset: int):
    return (
        db.query(ModelTask)
        .filter(ModelTask.status.in_(statuses))
        .order_by(desc(ModelTask.status), desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def not_assigned(db: Session, statuses: List[TaskStatus], limit: int, offset: int):
    subquery = (
        ~db.query(ModelAssignment.task_id)
        .filter(ModelAssignment.task_id == ModelTask.id)
        .exists()
    )
    return (
        db.query(ModelTask)
        .filter(ModelTask.status.in_(statuses))
        .filter(subquery)
        .order_by(desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def not_resolved(
    db: Session, user_id: UserId, statuses: List[TaskStatus], limit: int, offset: int
):
    return (
        db.query(ModelTask)
        .join(ModelAssignment)
        .filter(ModelTask.status.in_(statuses))
        .filter(ModelAssignment.user_id == user_id.id)
        .order_by(desc(ModelTask.status), desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
