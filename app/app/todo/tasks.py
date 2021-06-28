from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_task
from app.db.settings import db_session
from app.schemas.pager import Pager
from app.schemas.task import NOT_RESOLVED, Task, TaskCreate, TaskId, TaskUpdate

tasks = APIRouter(prefix="/tasks")


@tasks.get("/list", response_model=List[Task], tags=["tasks"])
async def list_tasks(pager: Pager = Depends(), db: Session = Depends(db_session)):
    """
    タスクをすべて取得する
    """
    return crud_task.all(db=db, limit=pager.per_page, offset=pager.offset())


@tasks.get("/get/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(task_id: int, db=Depends(db_session)):
    """
    IDを指定してタスクを1つ取得する
    """
    db_task = crud_task.find(db=db, task_id=TaskId(id=task_id))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@tasks.post("/create", response_model=Task, tags=["tasks"])
async def create_task(task: TaskCreate, db: Session = Depends(db_session)):
    """
    タスクを登録する
    """
    return crud_task.create(db=db, task=task)


@tasks.put("/update", response_model=Task, tags=["tasks"])
async def update_task(task: TaskUpdate, db: Session = Depends(db_session)):
    """
    タスクを更新する
    """
    return crud_task.update(db=db, task=task)


@tasks.get("/not_resolved", response_model=List[Task], tags=["tasks"])
async def not_resolved_tasks(
    pager: Pager = Depends(), db: Session = Depends(db_session)
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
    pager: Pager = Depends(), db: Session = Depends(db_session)
):
    """
    誰にもアサインされていない未完了のタスクを取得する
    優先度(高->低), ID(低->高)の順で出力される
    """
    return crud_task.not_assigned(
        db=db, statuses=NOT_RESOLVED, limit=pager.per_page, offset=pager.offset()
    )
