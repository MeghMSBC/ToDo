from sqlalchemy.orm import Session
import models
from models import User
import schemas
from passlib.context import CryptContext

def get_tasks(db:Session):
    return db.query(models.Task).all()

def get_task(db:Session,task_id:int):
    return db.query(models.Task).filter(models.Task.id==task_id).first()

def create_task(db:Session,task:schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db:Session,task_id:int,task:schemas.UpdateTask):
    db_task = get_task(db,task_id)
    if db_task:
        for key,value in task.dict(exclude_unset=True).items():
            setattr(db_task,key,value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db:Session,task_id:int):
    db_task= get_task(db,task_id)
    if(db_task):
        db.delete(db_task)
        db.commit()
    return db_task

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user