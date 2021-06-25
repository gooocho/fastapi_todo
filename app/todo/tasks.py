from fastapi.routing import APIRouter

from typing import List
from fastapi.routing import APIRouter

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud import crud_task
from app.repository.config import repository_session
from app.schemas.task import Task, TaskCreate


tasks = APIRouter(prefix="/tasks")


@tasks.get("/", response_model=List[Task], tags=["tasks"])
async def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    """
    タスクをすべて取得する
    """
    return crud_task.get_tasks(db, skip=skip, limit=limit)


@tasks.post("/", response_model=Task, tags=["tasks"])
async def create_task(task: TaskCreate, db: Session = Depends(repository_session)):
    """
    タスクを登録する
    """
    return crud_task.create_task(db=db, task=task)
