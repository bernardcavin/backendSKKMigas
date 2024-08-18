from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float
from enum import Enum as PyEnum
from backend.database import Base
from backend.routers.job.models import DataPhase, ValidationBase, CreateEditBase
import uuid


class EnvironmentType(PyEnum):
    MARINE = 'MARINE'
    LAND = 'LAND'
    SWAMP = 'SWAMP'

class DepthDatum(PyEnum):
    RT = 'RT'
    KB = 'KB'
    MSL = 'MSL'

class WellType(PyEnum):
    OIL = 'OIL'
    GAS = 'GAS'
    WATER = 'WATER'
    INJECTION = 'INJECTION'
    
class ProfileType(PyEnum):
    DIRECTIONAL = 'DIRECTIONAL'
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'
    
class WellClass(PyEnum):
    DELINEATION = "WILDCAT"
    WILDCAT = "DELINEATION"

class WellStatus(PyEnum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    ABANDONED = "Abandoned"
    ABANDONED_WHIPSTOCKED = "Abandoned Whipstocked"
    CAPPED = "Capped"
    POTENTIAL = "Potential"
    ABANDONED_JUNKED = "Abandoned Junked"
    NOT_DRILLED = "Not Drilled"
    CANCELLED = "Cancelled"
    UNKNOWN = "Unknown"

class CasingUOM(PyEnum):
    INCH = 'INCH'
    FEET = 'FEET'
    METER = 'METER'

class CasingType(PyEnum):
    CONDUCTOR_PIPE = 'CONDUCTOR PIPE'
    SURFACE_CASING = 'SURFACE CASING'
    INTERMEDIATE_CASING = 'INTERMEDIATE CASING'
    PRODUCTION_CASING = 'PRODUCTION CASING'
    PRODUCTION_LINER = 'PRODUCTION LINER'

class DepthUOM(PyEnum):
    FEET = 'FEET'
    METER = 'METER'

class VolumeUOM(PyEnum):
    FEET3 = 'FEET3'
    METER3 = 'METER3'

class MediaType(PyEnum):
    EXTERNAL_HARDDISK = 'EXTERNAL_HARDDISK'
    PAPER = 'PAPER'
    FILM = 'FILM'
    CDROM = 'CDROM'

class SizeUOM(PyEnum):
    BYTE = 'BYTE'
    KILOBYTE = 'KILOBYTE'
    MEGABYTE = 'MEGABYTE'

class LogType(PyEnum):
    GAMMA_RAY = 'GAMMA RAY'
    DENSITY = 'DENSITY'
    POROSITY = 'POROSITY'

class GRLogUOM(PyEnum):
    API = 'API'
    CPS = 'CPS'

class DENLogUOM(PyEnum):
    GRAM_PER_CC = 'G/CC'
    GRAM_PER_CM3 = 'G/CM3'
    KILOGRAM_PER_M3 = 'KG/M3'

class PORLogUOM(PyEnum):
    PERCENT = '%'
    DECIMAL = 'DECIMAL'

class Well(Base, ValidationBase, CreateEditBase):
    
    __tablename__ = 'wells'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    uwi = Column(String)
    field_id = Column(String(36), ForeignKey('fields.id')) 
    field = relationship('Field', back_populates='wells')

    kkks_id = Column(String(36), ForeignKey('kkks.id')) 
    kkks = relationship('KKKS', back_populates='wells')

    data_phase = Column(Enum(DataPhase))
    
    # Basic Information
    well_name = Column(String)
    alias_long_name = Column(String)
        
    # Well Status and Classification
    well_type = Column(Enum(WellType))
    well_class = Column(Enum(WellClass))
    well_status = Column(Enum(WellStatus))
    profile_type = Column(Enum(ProfileType))
    environment_type = Column(Enum(EnvironmentType))  # EnvironmentType Type (PPDM: ENVIRONMENT_TYPE)
    
    # Coordinates
    surface_longitude = Column(Float)  # Surface Longitude (PPDM: SURFACE_LONGITUDE)
    surface_latitude = Column(Float)  # Surface Latitude (PPDM: SURFACE_LATITUDE)
    bottom_hole_longitude = Column(Float)
    bottom_hole_latitude = Column(Float)
    maximum_inclination = Column(Float) #degrees
    maximum_azimuth = Column(Float) #degrees
        
    # Seismic Information
    line_name = Column(String)  # Line Name (PPDM: LINE_NAME)
    
    # Key Dates
    spud_date = Column(DateTime)  # Spud Date (PPDM: SPUD_DATE)
    final_drill_date = Column(DateTime)  # Final Drill Date (PPDM: FINAL_DRILL_DATE)
    completion_date = Column(DateTime)  # Completion Date (PPDM: COMPLETION_DATE)
    
    # Elevations
    rotary_table_elev = Column(Float)  # Rotary Table Elevation (PPDM: ROTARY_TABLE_ELEV)
    rotary_table_elev_ouom = Column(Enum(DepthUOM))  # Rotary Table Elevation ODepthUOM (PPDM: ROTARY_TABLE_ELEV_ODepthUOM)
    
    kb_elev = Column(Float)  # Kelly Bushing Elevation (PPDM: KB_ELEV)
    kb_elev_ouom = Column(Enum(DepthUOM))  # Kelly Bushing Elevation ODepthUOM (PPDM: KB_ELEV_ODepthUOM)
    
    derrick_floor_elev = Column(Float)  # Derrick Floor Elevation (PPDM: DERRICK_FLOOR_ELEV)
    derrick_floor_elev_ouom = Column(Enum(DepthUOM))  # Derrick Floor Elevation ODepthUOM (PPDM: DERRICK_FLOOR_ELEV_ODepthUOM)
    
    ground_elev = Column(Float)  # Ground Elevation (PPDM: GROUND_ELEV)
    ground_elev_ouom = Column(Enum(DepthUOM)) # Ground Elevation ODepthUOM (PPDM: GROUND_ELEV_ODepthUOM)
    
    mean_sea_level = Column(Float)
    mean_sea_level_ouom = Column(Enum(DepthDatum))
    
    # Depths
    depth_datum = Column(Enum(DepthDatum))  # Depth Datum (PPDM: DEPTH_DATUM)

    kick_off_point = Column(Float)
    kick_off_point_ouom = Column(Enum(DepthUOM))
    
    drill_td = Column(Float)  # Drill Total Depth (PPDM: DRILL_TD)
    drill_td_ouom = Column(Enum(DepthUOM))  # Drill Total Depth ODepthUOM (PPDM: DRILL_TD_ODepthUOM)
    
    log_td = Column(Float)  # Log Total Depth (PPDM: LOG_TD)
    log_td_ouom = Column(Enum(DepthUOM))  # Log Total Depth ODepthUOM (PPDM: LOG_TD_ODepthUOM)
    
    max_tvd = Column(Float)  # Maximum True Vertical Depth (PPDM: MAX_TVD)
    max_tvd_ouom = Column(Enum(DepthUOM))  # Maximum True Vertical Depth ODepthUOM (PPDM: MAX_TVD_ODepthUOM)
    
    projected_depth = Column(Float)  # Projected Depth (PPDM: PROJECTED_DEPTH)
    projected_depth_ouom = Column(Enum(DepthUOM))  # Projected Depth ODepthUOM (PPDM: PROJECTED_DEPTH_ODepthUOM)

    final_td = Column(Float)  # Final Total Depth (PPDM: FINAL_TD)
    final_td_ouom = Column(Enum(DepthUOM))  # Final Total Depth ODepthUOM (PPDM: FINAL_TD_ODepthUOM)

    remark = Column(Text)  # Remarks (PPDM: REMARK)
    
    well_documents = relationship('WellDocument', back_populates='well')
    # well_log_documents = relationship('WellLogDocument', back_populates='well')
    # well_samples = relationship('WellSample', back_populates='well')
    # well_core_samples = relationship('WellCoreSample', back_populates='well')
    well_casings = relationship('WellCasing', back_populates='well')
    well_trajectories = relationship('WellTrajectory', back_populates='well')
    well_ppfgs = relationship('WellPPFG', back_populates='well')
    well_logs = relationship('WellLog', back_populates='well')
    well_drilling_parameters = relationship('WellDrillingParameter', back_populates='well')
    well_strat = relationship('WellStrat', back_populates='well')
    
class WellDocument(Base):
    __tablename__ = 'well_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    file_id = Column(String(36), ForeignKey('files.id'), nullable=True)
    file = relationship('FileDB', foreign_keys=[file_id])

    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_documents')
    
    title = Column(String)
    
    media_type = Column(Enum(MediaType))
    document_type = Column(String)
    
    remark = Column(Text)

class DataClass(PyEnum):
    WELL_LOG='WELL LOG'
    TRAJECTORY='WELL TRAJECTORY'
    PPFG='PPFG'
    DRILLING_PARAMETER='DRILLING PARAMETER'

class WellDiigitalData(Base):

    __tablename__ = 'well_digital_data'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    well_id = Column(String(36), ForeignKey('wells.id'))

    file_id = Column(String(36), ForeignKey('files.id'), nullable=True)
    file = relationship('FileDB', foreign_keys=[file_id])

    data_class = Column(Enum(DataClass))

    __mapper_args__ = {
        'polymorphic_identity': 'well_digital_data',
        'polymorphic_on': data_class
    }

class WellLog(WellDiigitalData):

    __mapper_args__ = {
        'polymorphic_identity': DataClass.WELL_LOG,
    }

    well = relationship('Well', back_populates='well_logs')

class WellTrajectory(WellDiigitalData):

    __mapper_args__ = {
        'polymorphic_identity': DataClass.TRAJECTORY,
    }

    well = relationship('Well', back_populates='well_trajectories')

class WellPPFG(WellDiigitalData):

    __mapper_args__ = {
        'polymorphic_identity': DataClass.PPFG,
    }

    well = relationship('Well', back_populates='well_ppfgs')

class WellDrillingParameter(WellDiigitalData):

    __mapper_args__ = {
        'polymorphic_identity': DataClass.DRILLING_PARAMETER,
    }

    well = relationship('Well', back_populates='well_drilling_parameters')

class WellCasing(Base):
    __tablename__ = 'well_casings'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_casings')

    casing_type = Column(Enum(CasingType), nullable=True)
    grade = Column(String, nullable=True)
    inside_diameter = Column(Float, nullable=True)
    inside_diameter_ouom = Column(Enum(CasingUOM), nullable=True)
    outside_diameter = Column(Float, nullable=True)
    outside_diameter_ouom = Column(Enum(CasingUOM), nullable=True)
    base_depth = Column(Float, nullable=True)
    base_depth_ouom = Column(Enum(DepthUOM), nullable=True)

class WellStrat(Base):
    __tablename__ = 'well_strat'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'), nullable=True)
    well = relationship('Well', back_populates='well_strat')

    strat_unit_id = Column(String(36), ForeignKey('area_strat.id'), nullable=True)
    strat_unit = relationship('StratUnit', back_populates='well_strat')

    depth_datum = Column(Enum(DepthDatum), nullable=True)
    top_depth = Column(Float, nullable=True)
    bottom_depth = Column(Float, nullable=True)
    depth_uoum = Column(Enum(DepthUOM), nullable=True)
