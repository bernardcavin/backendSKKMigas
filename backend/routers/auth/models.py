from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
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
    jobs = relationship("Job", back_populates="kkks")
    area = relationship("Area", back_populates='kkks')
    well_instances = relationship("WellInstance", back_populates='kkks')

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), nullable=False)

    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship("KKKS", back_populates="users")

    verified_status = Column(Boolean)
