from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
import models, database
from datetime import datetime, timedelta
from logger import logger

# configuration for JWT tokens
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# password hashing and token configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password, hashed_password):
    """
    checks if a plain password matches a hashed password
    
    returns True if passwords match False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    hashes a password using bcrypt
    
    returns the hashed password
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    creates a JWT access token
    
    takes user data and optional expiration time
    returns the encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Access token created for user: {data.get('sub')}")
    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    gets the current authenticated user from token
    
    verifies the JWT token and retrieves user from database
    raises exception if token is invalid or user not found
    returns the authenticated user object
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token decoding failed: username missing")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWTError: {str(e)}")
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        logger.warning(f"User not found for token: {username}")
        raise credentials_exception
    logger.info(f"User authenticated: {username}")
    return user