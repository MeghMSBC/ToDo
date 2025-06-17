from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title : str 
    description:str=""
    completed :bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id:int

    class Config:
        orm_mode = True

class UpdateTask(BaseModel):
    title : Optional[str] = None
    description:Optional[str] = None
    completed :Optional[bool] = None


class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserLogin(BaseModel):
    username: str
    password: str
