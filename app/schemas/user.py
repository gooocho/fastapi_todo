from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    mail: str


class UserCreate(BaseUser):
    pass


class UserId(BaseModel):
    id: int


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
