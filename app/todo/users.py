from fastapi.routing import APIRouter

from typing import List
from fastapi.routing import APIRouter

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.repository.config import repository_session
from app.schemas.user import User
from app.schemas.user import UserCreate


users = APIRouter(prefix="/users")


@users.get("/", response_model=List[User], tags=["users"])
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    """
    ユーザーをすべて取得する
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@users.post("/", response_model=User, tags=["users"])
async def create_user(user: UserCreate, db: Session = Depends(repository_session)):
    """
    ユーザーを登録する
    """
    db_user = crud_user.get_user_by_mail(db, mail=user.mail)
    if db_user:
        raise HTTPException(status_code=400, detail="mail already registered")
    return crud_user.create_user(db=db, user=user)


@users.get("/{user_id}", response_model=User, tags=["users"])
async def read_user(user_id: int, db=Depends(repository_session)):
    """
    ユーザーIDを指定してユーザーを1つ取得する
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users.delete("/{user_id}", response_model=User, tags=["users"])
async def delete_user(user_id: int, db=Depends(repository_session)):
    """
    ユーザーを削除する
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db=db, user_id=user_id)
