from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Enum, Text, Float, Date
from enum import Enum as PyEnum
from app.api.visualize.lib.wellschematicspy.models import Casing
from app.core.database import Base
import uuid

from app.core.constants import uom, UnitType

class WellInstanceType(PyEnum):
    PROPOSED = 'PROPOSED'
    APPROVED = 'APPROVED'
    RETURNED = 'RETURNED'
    POST_OPERATION = 'POST OPERATION'
    PPP = 'PPP'

class EnvironmentType(PyEnum):
    MARINE = 'MARINE'
    LAND = 'LAND'
    SWAMP = 'SWAMP'

class DepthDatum(PyEnum):
    RT = 'RT'
    KB = 'KB'
    MSL = 'MSL'

class WellType(PyEnum):
    DELINEATION = "WILDCAT"
    WILDCAT = "DELINEATION"
    INJECTION = 'INJECTION'
    PRODUCER = 'PRODUCER'
    INFILL = 'INFILL'
    STEPOUT = 'STEPOUT'
    
class WellProfileType(PyEnum):
    DIRECTIONAL = 'DIRECTIONAL'
    VERTICAL = 'VERTICAL'

class WellDirectionalType(PyEnum):
    HORIZONTAL = 'HORIZONTAL'
    J_TYPE = 'J-TYPE'
    S_TYPE = 'S-TYPE'

class WellStatus(PyEnum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    ABANDONED = "Abandoned"
    TPA = 'Temporary P&A'
    PA = "P&A"

class CasingType(PyEnum):
    CONDUCTOR_PIPE = 'CONDUCTOR PIPE'
    SURFACE_CASING = 'SURFACE CASING'
    INTERMEDIATE_CASING = 'INTERMEDIATE CASING'
    PRODUCTION_CASING = 'PRODUCTION CASING'
    PRODUCTION_LINER = 'PRODUCTION LINER'

class MediaType(PyEnum):
    EXTERNAL_HARDDISK = 'EXTERNAL_HARDDISK'
    PAPER = 'PAPER'
    FILM = 'FILM'
    CDROM = 'CDROM'

class LogType(PyEnum):
    GAMMA_RAY = 'GAMMA RAY'
    DENSITY = 'DENSITY'
    POROSITY = 'POROSITY'

class DataClass(PyEnum):
    WELL_LOG='WELL LOG'
    TRAJECTORY='WELL TRAJECTORY'
    PPFG='PPFG'
    DRILLING_PARAMETER='DRILLING PARAMETER'

class HydrocarbonTarget(PyEnum):
    OIL = 'OIL'
    GAS = 'GAS'

class DataFormat(PyEnum):
    IMAGE = 'IMAGE'
    PDF = 'PDF'
    PLAIN_TEXT = 'PLAIN TEXT'
    
class WellInstance(Base):
    
    __tablename__ = 'well_instances'
    
    unit_type = Column(Enum(UnitType))

    well_instance_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    well_phase = Column(String(10))
    uwi = Column(String(50))
    
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship('Area', back_populates='well_instances')
    
    field_id = Column(String(36), ForeignKey('fields.id')) 
    field = relationship('Lapangan', back_populates='well_instances')

    kkks_id = Column(String(36), ForeignKey('kkks.id')) 
    kkks = relationship('KKKS', back_populates='well_instances')

    # actual= relationship('ActualWell', back_populates='well_instances')
    
    # Basic Information
    well_name = Column(String(50))
    alias_long_name = Column(String(50))
        
    # Well Status and Classification
    well_type = Column(Enum(WellType))
    well_profile_type = Column(Enum(WellProfileType))
    well_directional_type = Column(Enum(WellDirectionalType))
    hydrocarbon_target = Column(Enum(HydrocarbonTarget))
    environment_type = Column(Enum(EnvironmentType))
    
    # Coordinates
    surface_longitude = Column(Float)
    surface_latitude = Column(Float)
    bottom_hole_longitude = Column(Float)
    bottom_hole_latitude = Column(Float)
    maximum_inclination = Column(Float)
    azimuth = Column(Float)
        
    # Seismic Information
    line_name = Column(String(50))
    
    # Key Dates
    spud_date = Column(Date)
    final_drill_date = Column(Date)
    completion_date = Column(Date)
    
    # Elevations
    rotary_table_elev = Column(Float)
    rotary_table_elev_uom = Column(String(20))
    
    kb_elev = Column(Float)
    kb_elev_uom = Column(String(20))
    
    derrick_floor_elev = Column(Float)
    derrick_floor_elev_uom = Column(String(20))
    
    ground_elev = Column(Float)
    ground_elev_uom = Column(String(20))
    
    mean_sea_level = Column(Float)
    mean_sea_level_uom = Column(String(20))
    
    # Depths
    depth_datum = Column(Enum(DepthDatum))

    kick_off_point = Column(Float)
    kick_off_point_uom = Column(String(20))
    
    maximum_tvd = Column(Float)
    maximum_tvd_uom = Column(String(20))
    
    final_md = Column(Float)
    final_md_uom = Column(String(20))
    
    well_summary = relationship('WellSummary', back_populates='well_instance')
    well_trajectory = relationship('WellTrajectory', back_populates='well_instance', uselist=False)
    well_ppfg = relationship('WellPPFG', back_populates='well_instance', uselist=False)
    well_casing = relationship('WellCasing', back_populates='well_instance')
    well_schematic = relationship('WellSchematic', back_populates='well_instance', uselist=False)
    well_stratigraphy = relationship('WellStratigraphy', back_populates='well_instance')
    
    __mapper_args__ = {
        "polymorphic_on": "well_phase",
    }

    def __init__(self, unit_type,*args, **kwargs):

        # Set UOM fields based on unit_type
        uom_map = uom.get(unit_type, {})
        self.rotary_table_elev_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.kb_elev_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.derrick_floor_elev_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.ground_elev_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.mean_sea_level_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.kick_off_point_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.maximum_tvd_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.final_md_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        
        self.unit_type = unit_type

        super().__init__(*args, **kwargs)
    
class PlanWell(WellInstance):
    
    __tablename__ = 'well_plans'
    
    id = Column(String(36), ForeignKey('well_instances.well_instance_id'), primary_key=True)
    
    well_test = relationship('WellTest', back_populates='plan_well')

    __mapper_args__ = {
        "polymorphic_identity": "plan",
    }
    
class ActualWell(WellInstance):
    
    __tablename__ = 'well_actuals'
    
    id = Column(String(36), ForeignKey('well_instances.well_instance_id'), primary_key=True)
    well_documents = relationship('WellDocument', back_populates='actual_well')
    well_logs = relationship('WellLog', back_populates='actual_well')
    well_drilling_parameter = relationship('WellDrillingParameter', back_populates='actual_well', uselist=False)
    
    well_status = Column(Enum(WellStatus))
    
    remark = Column(Text)
    
    __mapper_args__ = {
        "polymorphic_identity": "actual",
    }

class WellDocumentType(PyEnum):
    WELL_REPORT = "Well Report"
    DRILLING_LOG = "Drilling Log"
    COMPLETION_REPORT = "Completion Report"
    WELLBORE_DIAGRAM = "Wellbore Diagram"
    WELL_TEST_REPORT = "Well Test Report"
    PRODUCTION_LOG = "Production Log"
    WELL_WORKOVER_REPORT = "Well Workover Report"
    WELLHEAD_INSPECTION = "Wellhead Inspection"
    CASING_REPORT = "Casing Report"
    CEMENTING_REPORT = "Cementing Report"
    PORE_PRESSURE_PREDICTION = "Pore Pressure Prediction"
    FRACTURE_GRADIENT_REPORT = "Fracture Gradient Report"
    WELL_TRAJECTORY = "Well Trajectory"
    LOGGING_REPORT = "Logging Report"
    MUD_LOGGING_REPORT = "Mud Logging Report"
    WELL_SITE_SURVEY = "Well Site Survey"
    GEOMECHANICAL_REPORT = "Geomechanical Report"
    RESERVOIR_CHARACTERIZATION = "Reservoir Characterization"
    CORE_ANALYSIS_REPORT = "Core Analysis Report"
    WELL_COMPLETION_SUMMARY = "Well Completion Summary"
    DRILLING_FLUID_REPORT = "Drilling Fluid Report"
    WELL_ABANDONMENT_REPORT = "Well Abandonment Report"
    HSE_REPORT = "HSE Report"

class WellDocument(Base):
    
    __tablename__ = 'well_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    file_id = Column(String(36), ForeignKey('files.id'), nullable=True)
    file = relationship('FileDB', foreign_keys=[file_id])

    actual_well_id = Column(String(36), ForeignKey('well_actuals.id'))
    actual_well = relationship('ActualWell', back_populates='well_documents')

    document_type = Column(Enum(WellDocumentType))
    
    remark = Column(Text)

class WellDigitalData(Base):

    __tablename__ = 'well_digital_data'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    file_id = Column(String(36), ForeignKey('files.id'), nullable=True)
    file = relationship('FileDB', foreign_keys=[file_id])
    
    # data_format = Column(Enum(DataFormat))
    data_class = Column(Enum(DataClass))

    __mapper_args__ = {
        'polymorphic_on': 'data_class'
    }

class WellLog(WellDigitalData):
    
    __tablename__ = 'well_digital_logs'
    
    id = Column(String(36), ForeignKey('well_digital_data.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': DataClass.WELL_LOG,
    }

    actual_well_id = Column(String(36), ForeignKey('well_actuals.id'))
    actual_well = relationship('ActualWell', back_populates='well_logs')

class WellTrajectory(WellDigitalData):
    
    __tablename__ = 'well_digital_trajectory'
    
    id = Column(String(36), ForeignKey('well_digital_data.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': DataClass.TRAJECTORY,
    }

    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'))
    well_instance = relationship('WellInstance', back_populates='well_trajectory', single_parent=True)

class WellPPFG(WellDigitalData):
    
    __tablename__ = 'well_digital_ppfg'
    
    id = Column(String(36), ForeignKey('well_digital_data.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': DataClass.PPFG,
    }

    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'))
    well_instance = relationship('WellInstance', back_populates='well_ppfg', single_parent=True)

class WellDrillingParameter(WellDigitalData):
    
    __tablename__ = 'well_digital_drilling_parameter'
    
    id = Column(String(36), ForeignKey('well_digital_data.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': DataClass.DRILLING_PARAMETER,
    }

    actual_well_id = Column(String(36), ForeignKey('well_actuals.id'))
    actual_well = relationship('ActualWell', back_populates='well_drilling_parameter', single_parent=True)

class WellSummaryMudType(PyEnum):
    WATER_BASED_MUD = 'WATER BASED MUD'
    OIL_BASED_MUD = 'OIL BASED MUD'

class WellSummary(Base):
    
    __tablename__ = 'well_summary'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    unit_type = Column(Enum(UnitType))
    
    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'), nullable=True)
    well_instance = relationship('WellInstance', back_populates='well_summary')

    depth_datum = Column(Enum(DepthDatum))  # Changed to String if not using Enums
    
    section_name = Column(String(50))
    
    top_depth = Column(Float)
    bottom_depth = Column(Float)
    depth_uom = Column(String(20))  # Changed to String if not using Enums
    
    hole_diameter = Column(Float)
    hole_diameter_uom = Column(String(20))  # Changed to String if not using Enums
    
    bit = Column(String(20))
    
    casing_outer_diameter = Column(Float)
    casing_outer_diameter_uom = Column(String(20))  # Changed to String if not using Enums
    
    logging = Column(String(255))
    
    # mud_program_id = Column(String(36), ForeignKey('well_summary_mud_program.id'))
    # mud_program = relationship('WellSummaryMudProgram', foreign_keys=[mud_program_id])
    
    # cementing_program_id = Column(String(36), ForeignKey('well_summary_cementing_program.id'))
    # cementing_program = relationship('WellSummaryCementingProgram', foreign_keys=[cementing_program_id])
    
    #mud_program
    mud_type = Column(Enum(WellSummaryMudType))
    mud_weight = Column(Float)
    mud_viscosity = Column(Float)
    mud_ph_level = Column(Float)
    
    #cementing program
    slurry_volume = Column(Float)
    slurry_mix = Column(String)
    
    bottom_hole_temperature = Column(Float)
    bottom_hole_temperature_uom = Column(String(20))
    
    rate_of_penetration = Column(Float)
    weight_on_bit = Column(Float)
    rotary_speed = Column(Float)
    
    remarks = Column(Text)

    def __init__(self, unit_type, *args, **kwargs):

        # Set uom fields based on unit_type
        uom_map = uom.get(unit_type, {})
        self.depth_uom = uom_map.get('Length', 'm')  # Default to meters if unit_type is not found
        self.hole_diameter_uom = uom_map.get('Diameter', 'mm')  # Default to mm if unit_type is not found
        self.casing_outer_diameter_uom = uom_map.get('Diameter', 'mm')  # Default to mm if unit_type is not found
        self.bottom_hole_temperature_uom = uom_map.get('Temperature', '°C')  # Default to °C if unit_type is not found
        
        self.unit_type = unit_type
        
        super().__init__(*args, **kwargs)

# class WellSummaryMudProgram(Base):
#     __tablename__ = 'well_summary_mud_program'
    
#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
#     mud_type = Column(Enum(MudType))
#     weight = Column(Float)
#     viscosity = Column(Float)
#     ph_level = Column(Float)

# class WellSummaryCementingProgram(Base):
#     __tablename__ = 'well_summary_cementing_program'
    
#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

#     slurry_volume = Column(Float)
#     slurry_mix = Column(String)

class WellTest(Base):
    __tablename__ = 'well_test'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    unit_type = Column(Enum(UnitType))
    
    well_id = Column(String(36), ForeignKey('well_plans.id'), nullable=True)
    plan_well = relationship('PlanWell', back_populates='well_test')
    
    depth_datum = Column(Enum(DepthDatum))  # Changed to String if not using Enums
    
    zone_name = Column(String(50))
    top_depth = Column(Float)
    bottom_depth = Column(Float)
    depth_uom = Column(String(50))  # Changed to String if not using Enums

    def __init__(self, unit_type, *args, **kwargs):
        
        # Set depth_uom based on unit_type
        uom_map = uom.get(unit_type, {})
        self.depth_uom = uom_map.get('Length', 'm')  # Default to meters if unit_type is not found
        
        self.unit_type = unit_type
        
        super().__init__(*args, **kwargs)

class WellCasing(Base):
    __tablename__ = 'well_casing'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'), nullable=True)
    well_instance = relationship('WellInstance', back_populates='well_casing')
    
    unit_type = Column(Enum(UnitType))
    
    casing_type = Column(Enum(CasingType))
    
    depth_datum = Column(Enum(DepthDatum))  # Changed to String if not using Enums
    depth = Column(Float)
    depth_uom = Column(String(20))  # Changed to String if not using Enums
    
    length = Column(Float)
    length_uom = Column(String(20))  # Changed to String if not using Enums
    
    hole_diameter = Column(Float)
    hole_diameter_uom = Column(String(20))  # Changed to String if not using Enums
    
    casing_outer_diameter = Column(Float)
    casing_outer_diameter_uom = Column(String(20))  # Changed to String if not using Enums
    
    casing_inner_diameter = Column(Float)
    casing_inner_diameter_uom = Column(String(20))  # Changed to String if not using Enums
    
    casing_grade = Column(String(50))
    
    casing_weight = Column(Float)
    casing_weight_uom = Column(String(20))  # Changed to String if not using Enums
    
    connection = Column(String(50))
    
    description = Column(Text)
    

    def __init__(self, unit_type, *args, **kwargs):
        
        # Set uom fields based on unit_type
        uom_map = uom.get(unit_type, {})
        self.depth_uom = uom_map.get('Length', 'm')
        self.length_uom = uom_map.get('Length', 'm')
        self.hole_diameter_uom = uom_map.get('Diameter', 'mm')
        self.casing_outer_diameter_uom = uom_map.get('Diameter', 'mm')
        self.casing_inner_diameter_uom = uom_map.get('Diameter', 'mm')
        self.casing_weight_uom = uom_map.get('Weight', 'kg')
        
        self.unit_type = unit_type
        
        super().__init__(*args, **kwargs)

class WellSchematic(Base):

    __tablename__ = 'job_well_schematics'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'), nullable=True)
    well_instance = relationship('WellInstance', back_populates='well_schematic')
    
    file_id = Column(String(36), ForeignKey('files.id'), nullable=True)
    file = relationship('FileDB', foreign_keys=[file_id])

class WellStratigraphy(Base):
    __tablename__ = 'well_stratigraphy'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    unit_type = Column(Enum(UnitType))
    
    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'))
    well_instance = relationship("WellInstance", back_populates='well_stratigraphy')
    
    depth_datum = Column(Enum(DepthDatum))
    
    top_depth = Column(Float)
    bottom_depth = Column(Float)
    depth_uom = Column(String(20))
    
    formation_name = Column(String(50))
    lithology = Column(String(255))

    def __init__(self, unit_type: str, *args, **kwargs):
        self.unit_type = unit_type

        # Set depth_uom based on unit_type
        if unit_type in uom and 'Length' in uom[unit_type]:
            self.depth_uom = uom[unit_type]['Length']
        else:
            self.depth_uom = 'm'  # Default value
        
        super().__init__(*args, **kwargs)