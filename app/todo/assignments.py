from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_assignment
from app.repository.config import repository_session
from app.schemas.assignment import Assignment, UserTaskPair

assignments = APIRouter(prefix="/assignments")


@assignments.post("/assign", response_model=UserTaskPair, tags=["assignments"])
async def assign(
    assignment: Assignment,
    db: Session = Depends(repository_session),
):
    """
    ユーザーとタスクを紐づける
    """
    db_user, db_task = crud_assignment.assign(
        db=db, assignment=assignment
    )
    return UserTaskPair(user=db_user, task=db_task)
