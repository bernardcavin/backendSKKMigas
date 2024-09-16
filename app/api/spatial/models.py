from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, JSON, Enum, Text
from enum import Enum as PyEnum
from app.core.database import Base
import uuid

class AreaPhase(PyEnum):
    EXPLORATION = "EXPLORATION"
    DEVELOPMENT = "DEVELOPMENT"

class AreaType(PyEnum):
    CONVENTIONAL = "CONVENTIONAL"
    NONCONVENTIONAL = "NON-CONVENTIONAL"

class AreaPosition(PyEnum):
    ONSHORE = "ONSHORE"
    OFFSHORE = "OFFSHORE"
    ONSHORE_AND_OFFSHORE = "ONSHORE AND OFFSHORE"

class AreaProductionStatus(PyEnum):
    NONPRODUCTION = 'NON-PRODUCTION'
    DEVELOPMENT = 'DEVELOPMENT'
    PRODUCTION = 'PRODUCTION'
    OFF = 'OFF NON-PRODUCTION'

class AreaRegion(PyEnum):
    REGION_I = 'REGION I'
    REGION_II = 'REGION II'
    REGION_III = 'REGION III'
    REGION_IV = 'REGION IV'
    REGION_V = 'REGION V'
    REGION_VI = 'REGION VI'
    
class StratType(PyEnum):
    LITHOSTRATIGRAPHIC = 'LITHOSTRATIGRAPHIC'
    CHRONOSTRATIGRAPHIC = 'CHRONOSTRATIGRAPHIC'
    BIOSTRATIGRAPHIC = 'BIOSTRATIGRAPHIC'
    RADIOMETRIC = 'RADIOMETRIC'
    OTHER = 'OTHER'

class StratUnitType(PyEnum):
    EON = 'EON'
    EPOCH = 'EPOCH'
    BED = 'BED'
    FORMATION = 'FORMATION'
    FAULT = 'FAULT'
    THRUST_SHEET = 'THRUST_SHEET'
    UNCONFORMITY = 'UNCONFORMITY'

class PetroleumSystem(PyEnum):
    SOURCE = 'SOURCE'
    RESERVOIR = 'RESERVOIR'
    SEAL = 'SEAL'
    OVERBURDEN = 'OVERBURDEN'

class Area(Base):
    
    __tablename__ = 'area'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    label = Column(String(50), unique=True)
    name = Column(String(50), unique=True, index=True)
    phase = Column(Enum(AreaPhase))
    type = Column(Enum(AreaType))
    position = Column(Enum(AreaPosition))
    production_status = Column(Enum(AreaProductionStatus))
    region = Column(Enum(AreaRegion))
    
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship("KKKS", back_populates='area')
    
    fields = relationship("Lapangan", back_populates="area")
    jobs = relationship("Job", back_populates='area')
    well_instances = relationship("WellInstance", back_populates='area')
    strat_units = relationship("StratUnit", back_populates="area")
    
    # geojson = Column(JSON)

class Lapangan(Base):   

    __tablename__ = 'fields'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String(50))
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship("Area", back_populates="fields")
    # geojson = Column(JSON)
    
    jobs = relationship("Job", back_populates='field')
    well_instances = relationship("WellInstance", back_populates="field")

class StratUnit(Base):
    
    __tablename__ = 'area_strat'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship("Area", back_populates="strat_units")
    
    strat_unit_name = Column(String(50))
    strat_type = Column(Enum(StratType))
    strat_unit_type = Column(Enum(StratUnitType))
    strat_petroleum_system = Column(Enum(PetroleumSystem))
    
    remark = Column(Text)
