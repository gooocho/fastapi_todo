from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_task, crud_user
from app.repository.config import repository_session
from app.schemas.pager import Pager
from app.schemas.task import NOT_RESOLVED, Task
from app.schemas.user import User, UserCreate, UserId, UserUpdate

users = APIRouter(prefix="/users")


@users.get("/list", response_model=List[User], tags=["users"])
async def list_users(
    pager: Pager = Depends(), db: Session = Depends(repository_session)
):
    """
    ユーザーをすべて取得する
    """
    users = crud_user.all(db=db, limit=pager.per_page, offset=pager.offset())
    return users


@users.get("/get/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: int, db=Depends(repository_session)):
    """
    IDを指定してユーザーを1つ取得する
    """
    db_user = crud_user.find(db=db, user_id=UserId(id=user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users.post("/create", response_model=User, tags=["users"])
async def create_user(user: UserCreate, db: Session = Depends(repository_session)):
    """
    ユーザーを登録する
    """
    db_user = crud_user.find_by_mail(db=db, mail=user.mail)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email address is already in use"
        )
    return crud_user.create(db=db, user=user)


@users.put("/update/", response_model=User, tags=["users"])
async def update_user(user: UserUpdate, db: Session = Depends(repository_session)):
    """
    ユーザーを更新する
    """
    db_user = crud_user.find_by_id(db=db, user_id=UserId(id=user.id))
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return crud_user.update(db=db, user=user)



@users.delete("/delete/", response_model=User, tags=["users"])
async def delete_user(user_id: int, db=Depends(repository_session)):
    """
    ユーザーを削除する
    """
    db_user = crud_user.find(db=db, user_id=UserId(id=user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete(db=db, user_id=user_id)


@users.get("/{user_id}/tasks/not_resolved", response_model=List[Task], tags=["users"])
async def not_resolved_tasks(
    user_id: int,
    pager: Pager = Depends(),
    db=Depends(repository_session),
):
    """
    ユーザーが担当している未完了のタスクを取得する
    ステータス(IN_PROGRESS -> NEW), 優先度(高->低), ID(低->高)の順で出力される
    """
    return crud_task.not_resolved(
        db=db,
        user_id=UserId(id=user_id),
        statuses=NOT_RESOLVED,
        limit=pager.per_page,
        offset=pager.offset(),
    )
