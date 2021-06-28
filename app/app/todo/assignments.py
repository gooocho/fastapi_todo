from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_assignment, crud_task, crud_user
from app.db.settings import db_session
from app.schemas.assignment import Assignment, AssignmentCreate
from app.schemas.task import TaskId
from app.schemas.user import UserId

assignments = APIRouter(prefix="/assignments")


@assignments.post("/create", response_model=Assignment, tags=["assignments"])
async def create(
    assignment: AssignmentCreate,
    db: Session = Depends(db_session),
):
    """
    ユーザーとタスクを紐づける
    """
    user_id = UserId(id=assignment.user_id)
    task_id = TaskId(id=assignment.task_id)

    db_user = crud_user.find(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_task = crud_task.find(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db_assignment = crud_assignment.find(db=db, user_id=user_id, task_id=task_id)
    if db_assignment is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment already presents"
        )

    return crud_assignment.create(db=db, assignment=assignment)
