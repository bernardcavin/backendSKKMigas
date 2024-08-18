from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float, Table
from enum import Enum as PyEnum
from backend.database import Base
import uuid

class FileDB(Base):

    __tablename__ = 'files'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    filename = Column(String)
    size  = Column(Integer)
    content_type = Column(String)
    upload_time = Column(DateTime)

    file_location = Column(String)

    uploaded_by_id = Column(String(36), ForeignKey('users.id'))
    uploaded_by = relationship('User', foreign_keys=[uploaded_by_id])
    

