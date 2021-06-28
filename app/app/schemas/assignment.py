from pydantic import BaseModel


class AssignmentBase(BaseModel):
    user_id: int
    task_id: int


class AssignmentCreate(AssignmentBase):
    pass


class Assignment(AssignmentBase):
    class Config:
        orm_mode = True
