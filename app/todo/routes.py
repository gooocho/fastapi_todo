from fastapi.routing import APIRouter

from typing import List
from fastapi.routing import APIRouter

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_user import get_user, get_users, get_user_by_mail, create_user
from app.crud.crud_task import get_tasks, create_task
from app.repository.config import repository_session
from app.schemas.user import User
from app.schemas.task import Task
from app.schemas.user import UserCreateReq
from app.schemas.task import TaskCreateReq


todos = APIRouter()


@todos.get("/users/", response_model=List[User])
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@todos.post("/users/", response_model=User)
async def create_user(user: UserCreateReq, db: Session = Depends(repository_session)):
    db_user = get_user_by_mail(db, mail=user.mail)
    if db_user:
        raise HTTPException(status_code=400, detail="mail already registered")
    # FIXME: not recursive
    return create_user(db=db, req=user)


@todos.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db=Depends(repository_session)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@todos.get("/tasks/", response_model=List[Task])
async def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(repository_session)
):
    return get_tasks(db, skip=skip, limit=limit)


@todos.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreateReq, db: Session = Depends(repository_session)):
    # FIXME: not recursive
    return create_task(db=db, task=task)
