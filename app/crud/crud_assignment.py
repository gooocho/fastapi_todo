from sqlalchemy.orm import Session

from app.models.user import User
from app.models.task import Task


def assign_task(db: Session, user_id: int, task_id: int):
    db_user = db.query(User).get(user_id)
    db_task = db.query(Task).get(task_id)
    db_user.tasks.append(db_task)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return [db_user, db_task]
