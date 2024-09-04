from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.routers.auth import models
import backend.routers.auth.schemas as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, kkks_id=user.kkks_id, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_by_kkks(db: Session, kkks_id: int):
    return db.query(models.User).filter(models.User.kkks_id == kkks_id).all()

def create_kkks(db: Session, kkks: schemas.CreateKKKS):
    db_kkks = models.KKKS(name = kkks.name)
    db.add(db_kkks)
    db.commit()
    db.refresh(db_kkks)
    return db_kkks

def get_kkks(db: Session, kkks_id: str):
    return db.query(models.KKKS).filter(models.KKKS.id == kkks_id).first()