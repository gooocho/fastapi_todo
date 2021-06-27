from pydantic import BaseModel, EmailStr


class UserId(BaseModel):
    id: int


class BaseUser(BaseModel):
    name: str
    mail: EmailStr


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
