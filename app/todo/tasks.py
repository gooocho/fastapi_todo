from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_task
from app.repository.config import repository_session
from app.schemas.pager import Pager
from app.schemas.task import NOT_RESOLVED, Task, TaskCreate

tasks = APIRouter(prefix="/tasks")


@tasks.get("/", response_model=List[Task], tags=["tasks"])
async def read_tasks(
    pager: Pager = Depends(), db: Session = Depends(repository_session)
):
    """
    タスクをすべて取得する
    """
    return crud_task.all(db=db, limit=pager.per_page, offset=pager.offset())


@tasks.post("/", response_model=Task, tags=["tasks"])
async def create_task(task: TaskCreate, db: Session = Depends(repository_session)):
    """
    タスクを登録する
    """
    return crud_task.create(db=db, task=task)


@tasks.get("/not_resolved", response_model=List[Task], tags=["tasks"])
async def not_resolved_tasks(
    pager: Pager = Depends(), db: Session = Depends(repository_session)
):
    """
    未完了のタスク(NEW / IN_PROGRESS)を取得する
    ステータス(IN_PROGRESS -> NEW), 優先度(高->低), ID(低->高)の順で出力される
    """
    return crud_task.filterd_by_status(
        db=db, statuses=NOT_RESOLVED, limit=pager.per_page, offset=pager.offset()
    )


@tasks.get("/not_assigned", response_model=List[Task], tags=["tasks"])
async def not_assigned_tasks(
    pager: Pager = Depends(), db: Session = Depends(repository_session)
):
    """
    誰にもアサインされていない未完了のタスクを取得する
    優先度(高->低), ID(低->高)の順で出力される
    """
    return crud_task.not_assigned(
        db=db, statuses=NOT_RESOLVED, limit=pager.per_page, offset=pager.offset()
    )
