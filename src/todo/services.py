from sqlalchemy.orm import Session

from .models.user import User
from .models.task import Task
from .schemas.user import UserCreateReq
from .schemas.task import TaskCreateReq


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, req: UserCreateReq):
    db_user = User(name=req.name, mail=req.mail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
