from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class Role(PyEnum):
    Admin = "Admin"
    User = "User"
    KKKS = "KKKS"

class KKKS(Base):
    __tablename__ = 'kkks'

    id = Column(String, primary_key=True, index=True)
    nama_kkks = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="kkks")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    kkks_id = Column(Integer, ForeignKey('kkks.id'))
    role = Column(Enum(Role), nullable=False)

    kkks = relationship("KKKS", back_populates="users")
