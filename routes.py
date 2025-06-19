from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, models, auth
from database import get_db
from auth import get_current_user, create_access_token
from datetime import timedelta
from logger import logger

router = APIRouter()

# user registration endpoint
@router.post("/signup", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    registers a new user account
    
    checks if username is available and creates a new user
    returns the created user object
    raises error if username is already taken
    """
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        logger.warning(f"Signup failed: username '{user.username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info(f"User registered: {user.username}")
    return crud.create_user(db, user)

# user login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    handles user login
    
    verifies username and password
    returns access token if credentials are correct
    raises error if credentials are invalid
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed for username: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    logger.info(f"Login successful for username: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

# get user's tasks
@router.get("/tasks", response_model=list[schemas.Task])
def get_user_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    retrieves all tasks for the current user
    
    returns a list of tasks
    """
    return crud.get_tasks(db, current_user.id)

# create new task
@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    creates a new task for the current user
    
    returns the created task object
    """
    return crud.create_task(db, task, current_user.id)

# update existing task
@router.put("/{task_id}", response_model=schemas.Task)  
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    updates an existing task
    
    returns the updated task
    raises error if task not found or user unauthorized
    """
    updated_task = crud.update_task(db, task_id, task, current_user.id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    return updated_task

# delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    deletes a task
    
    returns success message
    raises error if task not found
    """
    deleted = crud.delete_task(db, task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

