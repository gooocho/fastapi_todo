from typing import Optional

from pydantic import BaseModel, EmailStr


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
