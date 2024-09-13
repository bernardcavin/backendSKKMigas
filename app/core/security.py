from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api.auth import models
from app.core.database import SessionLocal
from typing import Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from app.api.auth import crud, models
from datetime import datetime, timezone
from functools import wraps
from app.core.config import settings

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="{settings.API_V1_STR}/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=user_name)
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user is not None:
                # Check user's role
                user_role = user.role
                if user_role not in role:
                    raise HTTPException(status_code=403, detail="User is not authorized to access this resource")
                
                # Check if user is verified
                user_is_verified = user.verified_status
                if not user_is_verified:
                    raise HTTPException(status_code=403, detail="User is not verified")
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")
            return await func(*args, **kwargs)
        return wrapper
    return decorator