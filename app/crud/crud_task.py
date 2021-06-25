from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreateReq


def get_tasks(db: Session, skip: int, limit: int):
    return db.query(Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreateReq):
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
