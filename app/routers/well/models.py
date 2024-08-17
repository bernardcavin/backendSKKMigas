from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float
from enum import Enum as PyEnum
from app.database import Base
from app.routers.job.models import DataPhase, ValidationBase, CreateEditBase
import uuid


class Environment(PyEnum):
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
    ACTIVE = ("ACT", "A well which is in active operation in accordance with the purpose for which it is licensed.")
    SUSPENDED = ("SUS", "A well that failed to achieve or is no longer being used for its licensed purpose, and the well has not been plugged.")
    ABANDONED = ("ABD", "A well which is officially plugged and abandoned.")
    ABANDONED_WHIPSTOCKED = ("ABW", "A well drilled and plugged back and another hole drilled and whipstocked out of the same well bore.")
    CAPPED = ("CAP", "A well with proven productivity (by test or judgment) which has not been placed on production.")
    POTENTIAL = ("POT", "A newly-drilled or recompleted well in which suitability for production, injection or storage is assumed but not proven. This mode is applicable for a maximum of 12 months after the TD date or recompletion date of the well.")
    ABANDONED_JUNKED = ("LOS", "A well abandoned because of mechanical difficulties in the hole.")
    NOT_DRILLED = ("NDR", "A location for which a well licence has been issued but a well has not yet been drilled.")
    CANCELLED = ("CAN", "A location for which a well licence was issued but the licence has been cancelled.")
    UNKNOWN = ("UNK", "A well for which there is no available information on mode in Ministry records.")
    NO_WELL_FOUND = ("NWF", "A well that could not be located in the field by a petroleum inspector.")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.code}): {self.description}"
    
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
    environment_type = Column(Enum(Environment))  # Environment Type (PPDM: ENVIRONMENT_TYPE)
    
    # Coordinates
    surface_longitude = Column(Float)  # Surface Longitude (PPDM: SURFACE_LONGITUDE)
    surface_latitude = Column(Float)  # Surface Latitude (PPDM: SURFACE_LATITUDE)
    bottom_hole_longitude = Column(Float)
    bottom_hole_latitude = Column(Float)
        
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
    
    documents = relationship('WellDocument', back_populates='well')
    well_log_documents = relationship('WellLogDocument', back_populates='well')
    well_samples = relationship('WellSample', back_populates='well')
    well_core_samples = relationship('WellCoreSample', back_populates='well')
    well_casing = relationship('WellCasing', back_populates='well')
    well_trajectory = relationship('WellTrajectory', back_populates='well')
    well_ppfg = relationship('PorePressureFractureGradient', back_populates='well')
    well_logs = relationship('WellLog', back_populates='well')
    well_drilling_parameter = relationship('DrillingParameter', back_populates='well')
    well_strat = relationship('WellStrat', back_populates='well')
    
class WellDocument(Base):
    __tablename__ = 'well_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='documents')
    
    title = Column(String)
    creator_name = Column(String)
    create_date = Column(DateTime)
    
    media_type = Column(Enum(MediaType))
    document_type = Column(String)
    
    item_category = Column(String)
    item_sub_category = Column(String)
    
    digital_format = Column(String)
    
    original_file_name = Column(String)
    
    digital_size = Column(Float)
    digital_size_uom = Column(Enum(SizeUOM))
    
    remark = Column(Text)

class WellLogDocument(Base):
    
    __tablename__ = 'well_log_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_log_documents')
    
    logging_company = Column(String)
    media_type = Column(Enum(MediaType))

    log_title = Column(String)
    digital_format = Column(String)
    report_log_run = Column(String)
    
    trip_date = Column(DateTime)
    top_depth = Column(Float)
    top_depth_ouom = Column(Enum(DepthUOM))
    
    base_depth = Column(Float)
    base_depth_ouom = Column(Enum(DepthUOM))
    
    original_file_name = Column(String)

    digital_size = Column(Float)
    digital_size_uom = Column(Enum(SizeUOM))
    
    remark = Column(Text)

class WellSample(Base):
    
    __tablename__ = 'well_samples'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_samples')
    
    sample_type = Column(String)
    sample_num = Column(String)
    sample_count = Column(Integer)
    
    top_md = Column(Float)
    top_md_ouom = Column(Enum(DepthUOM))
    
    base_md = Column(Float)
    base_md_ouom = Column(Enum(DepthUOM))
    
    study_type = Column(String)

    remark = Column(Text)

class WellCoreSample(Base):
    
    __tablename__ = 'well_core_samples'

    id = Column(Integer, primary_key=True, autoincrement=True)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_core_samples')
    
    core_type = Column(String)
    sample_num = Column(String)
    sample_count = Column(Integer)
    
    top_depth = Column(Float)
    top_depth_ouom = Column(Enum(DepthUOM))
    
    base_depth = Column(Float)
    base_depth_ouom = Column(Enum(DepthUOM))
    
    portion_volume = Column(Float)
    portion_volume_ouom = Column(Enum(VolumeUOM))
    
    study_type = Column(String)
    
    remark = Column(Text)

class WellCasing(Base):
    
    __tablename__ = 'well_casings'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_casing')

    casing_type = Column(Enum(CasingType))
    grade = Column(String)
    
    inside_diameter = Column(Float)
    inside_diameter_ouom = Column(Enum(CasingUOM))
    
    outside_diameter = Column(Float)
    outside_diameter_ouom = Column(Enum(CasingUOM))
    
    base_depth = Column(Float)
    base_depth_ouom = Column(Enum(CasingUOM))

class WellTrajectory(Base):
    
    __tablename__ = 'well_trajectories'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_trajectory')

    measured_depth = Column(Float)  # Measured Depth
    true_vertical_depth = Column(Float)  # True Vertical Depth
    true_vertical_depth_sub_sea = Column(Float)  # True Vertical Depth Subsea
    
    inclination = Column(Float)  # Inclination
    azimuth = Column(Float)  # Azimuth Grid
    
    latitude = Column(Float)  # Latitude
    longitude = Column(Float)  # Longitude

class PorePressureFractureGradient(Base):
    
    __tablename__ = 'well_ppfg'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_ppfg')
    
    depth_datum = Column(Enum(DepthDatum))
    depth = Column(Float)
    depth_uoum = Column(Enum(DepthUOM))
    
    overburden_stress = Column(Float)
    pore_pressure = Column(Float)
    fracture_pressure = Column(Float)

class WellLog(Base):
    
    __tablename__ = 'well_log'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_logs')
    
    depth_datum = Column(Enum(DepthDatum))
    depth = Column(Float)
    depth_uoum = Column(Enum(DepthUOM))
    
    gamma_ray_log_name = Column(String)
    gamma_ray_log = Column(Float)
    gamma_ray_log_ouom = Column(Enum(GRLogUOM))
    
    density_log_name = Column(String)
    density_log = Column(Float)
    density_log_ouom = Column(Enum(DENLogUOM))
    
    porosity_log_name = Column(String)
    porosity_log = Column(Float)
    porosity_log_ouom = Column(Enum(PORLogUOM))

class DrillingParameter(Base):
    
    __tablename__ = 'well_drilling_parameter'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_drilling_parameter')
    
    depth_datum = Column(Enum(DepthDatum))
    depth = Column(Float)
    depth_uoum = Column(Enum(DepthUOM))
    
    rate_of_penetration = Column(Float)
    weight_on_bit = Column(Float)
    hookload = Column(Float)
    top_drive = Column(Float)
    mud_motor = Column(Float)
    total_rpm = Column(Float)
    torque = Column(Float)
    mud_weight = Column(Float)

class WellStrat(Base):
    
    __tablename__ = 'well_strat'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship('Well', back_populates='well_strat')
    
    strat_unit_id = Column(String(36), ForeignKey('area_strat.id'))
    strat_unit = relationship('StratUnit', back_populates='well_strat')
    
    depth_datum = Column(Enum(DepthDatum))
    top_depth = Column(Float)
    bottom_depth = Column(Float)
    depth_uoum = Column(Enum(DepthUOM))
    
