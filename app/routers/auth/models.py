from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum
import uuid

class Role(PyEnum):
    Admin = "Admin"
    User = "User"
    KKKS = "KKKS"

class KKKS(Base):
    __tablename__ = 'kkks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    nama_kkks = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="kkks")
    well = relationship("Well", back_populates="kkks")

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    kkks_id = Column(Integer, ForeignKey('kkks.id'))
    role = Column(Enum(Role), nullable=False)

    kkks = relationship("KKKS", back_populates="users")
