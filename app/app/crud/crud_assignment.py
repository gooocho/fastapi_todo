from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.assignment import Assignment


def assign(db: Session, assignment: Assignment):
    db_user = db.query(User).get(assignment.user_id)
    db_task = db.query(Task).get(assignment.task_id)
    db_user.tasks.append(db_task)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return [db_user, db_task]
