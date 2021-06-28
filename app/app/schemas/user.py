from pydantic import BaseModel, EmailStr
from typing import Optional


class UserId(BaseModel):
    id: int


class BaseUser(BaseModel):
    name: str
    mail: EmailStr


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    id: int
    name: Optional[str]
    mail: Optional[EmailStr]


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
