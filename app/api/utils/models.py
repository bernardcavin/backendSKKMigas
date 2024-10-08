from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float, Table
from enum import Enum as PyEnum
from app.core.database import Base
import uuid

class FileDB(Base):

    __tablename__ = 'files'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    filename = Column(String(255))
    file_location = Column(String(255))
    file_extension = Column(String(5))

    uploaded_by_id = Column(String(36), ForeignKey('users.id'))
    uploaded_by = relationship('User', foreign_keys=[uploaded_by_id])