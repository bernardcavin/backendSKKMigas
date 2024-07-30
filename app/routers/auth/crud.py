from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.routers.auth import models
import app.routers.auth.schemas as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, kkks_id=user.kkks_id, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_by_kkks(db: Session, kkks_id: int):
    return db.query(models.User).filter(models.User.kkks_id == kkks_id).all()

def generate_kkks_id(session, prefix='KKKS', length=4):
    # Query to get the latest KKKS record based on the ID
    last_record = session.query(models.KKKS).order_by(models.KKKS.id.desc()).first()
    
    if last_record:
        last_id = last_record.id
        number = int(last_id[len(prefix):]) + 1
    else:
        number = 1
    
    # Format the new ID
    new_id = f"{prefix}{number:0{length}}"
    return new_id

def create_kkks(db: Session, kkks: schemas.KKKSCreate):
    db_kkks = models.KKKS(id=generate_kkks_id(db),nama_kkks = kkks.nama_kkks)
    db.add(db_kkks)
    db.commit()
    db.refresh(db_kkks)
    return db_kkks

def get_kkks(db: Session, kkks_id: str):
    return db.query(models.KKKS).filter(models.KKKS.id == kkks_id).first()