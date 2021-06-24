from pydantic import BaseModel


class UserCreateReq(BaseModel):
    name: str
    mail: str


class User(BaseModel):
    id: int
    name: str
    mail: str

    class Config:
        orm_mode = True
