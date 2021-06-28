from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate
from app.schemas.task import TaskId
from app.schemas.user import UserId


def find(db: Session, user_id: UserId, task_id: TaskId):
    return (
        db.query(Assignment)
        .filter(Assignment.user_id == user_id.id)
        .filter(Assignment.task_id == task_id.id)
        .first()
    )


def create(db: Session, assignment: AssignmentCreate):
    db_assignment = Assignment(user_id=assignment.user_id, task_id=assignment.task_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
