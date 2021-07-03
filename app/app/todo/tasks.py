from typing import List

from fastapi import Depends, HTTPException, status
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
    条件を指定せずタスクを取得する。
    """
    return crud_task.all(db=db, limit=pager.per_page, offset=pager.offset())


@tasks.get("/get/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(task_id: int, db=Depends(db_session)):
    """
    IDを指定してタスクを１件取得する。
    """
    model_task = crud_task.find(db=db, task_id=TaskId(id=task_id))
    if model_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return model_task


@tasks.post(
    "/create", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"]
)
async def create_task(task: TaskCreate, db: Session = Depends(db_session)):
    """
    タスクを１件登録する。
    """
    return crud_task.create(db=db, task=task)


@tasks.put("/update", response_model=Task, tags=["tasks"])
async def update_task(task: TaskUpdate, db: Session = Depends(db_session)):
    """
    タスクを１件更新する。
    """
    model_task = crud_task.find(db=db, task_id=TaskId(id=task.id))
    if model_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return crud_task.update(db=db, task=task)


@tasks.get("/not_resolved", response_model=List[Task], tags=["tasks"])
async def not_resolved_tasks(
    pager: Pager = Depends(), db: Session = Depends(db_session)
):
    """
    未完了(NEW / IN_PROGRESS)のタスクを取得する。

    1. ステータスが進んでいるもの（（進んでいる）作業中 > 未着手（進んでいない））
    2. 優先度が大きいもの
    3. ID が小さいもの
    の順で出力される。
    """
    return crud_task.filterd_by_status(
        db=db, statuses=NOT_RESOLVED, limit=pager.per_page, offset=pager.offset()
    )


@tasks.get("/not_assigned", response_model=List[Task], tags=["tasks"])
async def not_assigned_tasks(
    pager: Pager = Depends(), db: Session = Depends(db_session)
):
    """
    どのユーザーにもアサインされていない、未完了(NEW / IN_PROGRESS)のタスクを取得する。
    1. 優先度が大きいもの
    2. ID が小さいもの
    の順で出力される。
    """
    return crud_task.not_assigned(
        db=db, statuses=NOT_RESOLVED, limit=pager.per_page, offset=pager.offset()
    )
