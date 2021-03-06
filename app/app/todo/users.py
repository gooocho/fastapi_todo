from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_task, crud_user
from app.db.settings import db_session
from app.schemas.pager import Pager
from app.schemas.task import NOT_RESOLVED, Task
from app.schemas.user import User, UserCreate, UserId, UserUpdate

users = APIRouter(prefix="/users")


@users.get("/list", response_model=List[User], tags=["users"])
async def list_users(pager: Pager = Depends(), db: Session = Depends(db_session)):
    """
    条件を指定せずユーザーを取得する。
    """
    model_users = crud_user.all(db=db, limit=pager.per_page, offset=pager.offset())
    return model_users


@users.get("/get/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: int, db=Depends(db_session)):
    """
    IDを指定してユーザーを１件取得する。
    """
    model_user = crud_user.find(db=db, user_id=UserId(id=user_id))
    if model_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return model_user


@users.post(
    "/create", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"]
)
async def create_user(user: UserCreate, db: Session = Depends(db_session)):
    """
    ユーザーを１件登録する。
    """
    model_user = crud_user.find_by_mail(db=db, mail=user.mail)
    if model_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already in use",
        )
    return crud_user.create(db=db, user=user)


@users.put("/update", response_model=User, tags=["users"])
async def update_user(user: UserUpdate, db: Session = Depends(db_session)):
    """
    ユーザーを１件更新する。
    """
    model_user = crud_user.find(db=db, user_id=UserId(id=user.id))
    if model_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud_user.update(db=db, user=user)


@users.delete(
    "/delete/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
async def delete_user(user_id: int, db=Depends(db_session)):
    """
    ユーザーを１件削除する。
    """
    model_user = crud_user.find(db=db, user_id=UserId(id=user_id))
    if model_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    crud_user.delete(db=db, user_id=UserId(id=user_id))


@users.get("/{user_id}/tasks/not_resolved", response_model=List[Task], tags=["users"])
async def not_resolved_tasks(
    user_id: int,
    pager: Pager = Depends(),
    db=Depends(db_session),
):
    """
    ユーザーが担当している未完了のタスクを取得する。

    1. ステータスが進んでいるもの（（進んでいる）完了 > 作業中 > 未着手（進んでいない））
    2. 優先度が大きいもの
    3. ID が小さいもの
    の順で出力される。
    """
    model_user = crud_user.find(db=db, user_id=UserId(id=user_id))
    if model_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud_task.with_user_filtered_by_statuses(
        db=db,
        user_id=UserId(id=user_id),
        statuses=NOT_RESOLVED,
        limit=pager.per_page,
        offset=pager.offset(),
    )
