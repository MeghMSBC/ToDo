from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, models, auth
from database import get_db
from auth import get_current_user, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/tasks", response_model=list[schemas.Task])
def get_user_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_tasks(db, current_user.id)

@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db, task, current_user.id)


@router.put("/{task_id}", response_model=schemas.Task)  
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_task = crud.update_task(db, task_id, task, current_user.id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    return updated_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

