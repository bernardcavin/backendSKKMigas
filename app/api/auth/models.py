from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum
import uuid

class Role(PyEnum):
    Admin = "Admin"
    KKKS = "KKKS"

class KKKS(Base):
    __tablename__ = 'kkks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String, unique=True, index=True)
    users = relationship("KKKSUser", back_populates="kkks")
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
    
    verified_status = Column(Boolean)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role
    }
    
class Admin(User):
    __tablename__ = 'user_admin'
    
    id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": Role.Admin,
    }

class KKKSUser(User):
    __tablename__ = 'user_kkks'
    
    id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship("KKKS", back_populates="users")
    
    __mapper_args__ = {
        "polymorphic_identity": Role.KKKS
    }
