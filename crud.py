import models, schemas
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password
from logger import logger

# create a new user in the database
# takes user data and creates a new user record with hashed password
def create_user(db: Session, user: schemas.UserCreate):
    """
    creates a new user in the database
    
    takes user data and creates a new user record with hashed password
    
    returns the created user object
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"New user created: {user.username}")
    return db_user

# authenticate a user by checking username and password
def authenticate_user(db: Session, username: str, password: str):
    """
    checks if a user exists with the given username and password
    
    returns the user object if credentials are correct
    returns None if credentials are invalid
    """
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        logger.info(f"User authenticated successfully: {username}")
        return user
    logger.warning(f"Authentication failed for user: {username}")
    return None

# create a new task for a user
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """
    creates a new task for the specified user
    
    adds the task to the database and returns the created task
    """
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created for user_id={user_id}: {task.title}")
    return db_task

# get all tasks for a user
def get_tasks(db: Session, user_id: int):
    """
    retrieves all tasks for a specific user
    
    returns a list of task objects
    """
    logger.info(f"Fetching tasks for user_id={user_id}")
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

# get a specific task by id
def get_task(db: Session, task_id: int, user_id: int):
    """
    retrieves a specific task by its id and user
    
    returns the task if it exists and belongs to the user
    """
    logger.info(f"Fetching task {task_id} for user_id={user_id}")
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()

# update an existing task
def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate, user_id: int):
    """
    updates an existing task with new data
    
    returns the updated task if it exists and belongs to the user
    """
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not task:
        logger.warning(f"Task update failed. Task {task_id} not found for user_id={user_id}")
        return None

    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    logger.info(f"Task {task_id} updated for user_id={user_id}")
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        logger.info(f"Task {task_id} deleted for user_id={user_id}")
    else:
        logger.warning(f"Delete failed. Task {task_id} not found for user_id={user_id}")
    return db_task