from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_assignment
from app.repository.config import repository_session
from app.schemas.assignment import UserTaskPair

assignments = APIRouter(prefix="/assignments")


@assignments.post("/assign", response_model=UserTaskPair, tags=["assignments"])
async def assign(user_id: int, task_id: int, db: Session = Depends(repository_session)):
    """
    ユーザーとタスクを紐づける
    """
    db_user, db_task = crud_assignment.assign(db=db, user_id=user_id, task_id=task_id)
    return UserTaskPair(user=db_user, task=db_task)
