from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float, Table, Date, func
from backend.routers.well.models import DepthUOM, DepthDatum, MediaType, SizeUOM
from sqlalchemy.orm import relationship, declared_attr
from backend.database import Base
from enum import Enum as PyEnum
import uuid

class Severity(PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class WOWSJobType(PyEnum):
    ACID_FRACTURING = 'Acid Fracturing'
    ADD_PERFORATION = 'Add Perforation'
    ADDITIONAL_PERFOR_NEW_PERFO = 'Aditional Perfor & New Perfo'
    CTG = 'CTG'
    CTI = 'CTI'
    CTO = 'CTO'
    CHANGE_LAYER = 'Change Layer'
    CONVERSION_INJECTOR_TO_PRODUCER = 'Conversion from Injector to Producer'
    CONVERT_TO_INJECTOR = 'Convert to Injector'
    ESP_INSTALLATION = 'ESP Installation'
    FRACT_PACK = 'Fract Pack'
    FRACTURING = 'Fracturing'
    GLV_INSTALLATION = 'GLV Installation'
    GTO = 'GTO'
    HPU_INSTALLATION = 'HPU Installation'
    HYDRAULIC_FRACTURING = 'Hydraulic Fracturing'
    INSTALL_ESP = 'Install ESP'
    INSTALL_HPU = 'Install HPU'
    NEW_PERFORATION = 'New Perforation'
    NEW_ZONE_BEHIND_PIPE = 'New Zone Behind Pipe'
    PA = 'P&A'
    PCTGL = 'PCTGL'
    POP = 'POP'
    PUT_ON_PRODUCTION = 'Put On Production'
    RE_PERFORATION_ACID_FRACTURING = 'Re-perforation & Acid Fracturing'
    REACTIVATION_WELL = 'Reactivation Well'
    REACTIVATION_RECOMPLETION = 'Reactivation and Recompletion'
    RECOMPLETION = 'Recompletion'
    RECOMPLETION_REPERFORATION = 'Recompletion and Reperforation'
    RETUBING = 'Retubing'
    SCON = 'SCON'
    SRP_INSTALLATION = 'SRP Installation'
    SAND_CLEANOUT_ADD_PERFORATION_SAND_SCREEN = 'Sand Cleanout - Add Perforation - Sand Screen'
    STIMULATION_CHANGE_LAYER = 'Stimulation & Change Layer'
    STIMULATION_ACIDIZING = 'Stimulation / Acidizing'
    THRU_TUBING_PERFORATION = 'Thru Tubing Perforation'
    WATER_SHUT_OFF_CHANGE_LAYER = 'Water Shut Off & Change Layer'
    # SQUEEZE_CEMENTING = ''
    # FISHING_JOB
    # PASANG/GANTI KEDALAMAN POSISI ESP ERP HPU
    # PRODUCTION PACKER INSTALASI
    # GANTI BIN PUMPING
    # SAND CONTROL DESIGN
    # SCALE CONTROL
    # PERBAIKAN CASING/TUBING BOCOR

    # PUMPING SAND CLEAN OUT
    # HANTI SUCK ROD
    # GANTI TUBING PECAH
    # GANTI ESP
    # GANTI ESP CABLE
    # GANTI POSISI DAN UKURAN GAS LIFT VALVE
    # GANTI GATE VALVE
    # PERBAIKAN ELECTRIC MOTOR

class ContractType(PyEnum):
    COST_RECOVERY = 'COST-RECOVERY'
    GROSS_SPLIT = 'GROSS-SPLIT'

class RigType(PyEnum):
    JACK_UP = 'JACK-UP'
    BARGE = 'BARGE'
    FLOATER = 'FLOATER'
    SEMI_SUBMERSIBLE = 'SEMI-SUBMERSIBLE'
    DRILLSHIP = 'DRILLSHIP'

class JobInstanceType(PyEnum):
    INITIAL_PROPOSAL = 'INITIAL PROPOSAL'
    REVISION = 'REVISION'
    POST_OPERATION = 'POST OPERATION'
    PPP = 'PPP'

class HazardType(PyEnum):
    GAS_KICK = "GAS KICK"
    STUCK_PIPE = "STUCK PIPE"
    LOST_CIRCULATION = "LOST CIRCULATION"
    WELL_CONTROL = "WELL CONTROL"
    EQUIPMENT_FAILURE = "EQUIPMENT FAILURE"
    OTHER = "OTHER"

class CreateBase:
    
    time_created = Column(DateTime, default=func.now())
    
    @declared_attr
    def created_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])

class EditBase:
    
    last_edited = Column(DateTime, onupdate=func.utc_timestamp())
    
    @declared_attr
    def last_edited_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class Job(Base):
    
    __tablename__ = 'jobs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_instance_type = Column(Enum(JobInstanceType))
    job_type = Column(String)
    
    #kkks information
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship('KKKS', back_populates='jobs')
    
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship('Area', back_populates='jobs')
    
    field_id = Column(String(36), ForeignKey('fields.id'))
    field = relationship('Field', back_populates='jobs')
    
    #contract information
    contract_type = Column(Enum(ContractType))
    
    afe_number = Column(String)
    wpb_year = Column(Integer)
    
    start_date = Column(Date)
    end_date = Column(Date)
    total_budget = Column(Numeric(precision=10, scale=2))

    # rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    # job activity
    job_operation_days = relationship('JobOperationDay', back_populates='job')
    work_breakdown_structure = relationship('WorkBreakdownStructure', back_populates='job')
    job_hazards = relationship('JobHazard', back_populates='job')
    job_documents = relationship('JobDocument', back_populates='job')
    
    __mapper_args__ = {
        "polymorphic_identity": "job",
        "polymorphic_on": "job_type",
    }

class WorkBreakdownStructure(Base):
    
    __tablename__ = 'job_wbs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='work_breakdown_structure')
    
    event = Column(String)
    start_date = Column(Date)
    end_data = Column(Date)
    remarks = Column(Text)

class JobHazard(Base):
    
    __tablename__ = 'job_hazards'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_hazards')
    
    hazard_type = Column(Enum(HazardType))
    hazard_description = Column(Text)
    severity = Column(Enum(Severity))
    mitigation = Column(Text)
    
    remark = Column(Text)

class JobDocument(Base):
    
    __tablename__ = 'job_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_documents')

    file_id = Column(String(36), ForeignKey('files.id'))
    file = relationship('FileDB', foreign_keys=[file_id])
    
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

class JobOperationDay(Base):
    
    __tablename__ = 'job_operation_days'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    phase = Column(String)
    
    depth_datum = Column(Enum(DepthDatum))
    
    depth_in = Column(Float)
    depth_out = Column(Float)
    depth_uoum = Column(Enum(DepthUOM))
    
    operation_days = Column(Float)
    
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_operation_days')

class ValidationBase:
    
    validation_date = Column(DateTime)
    
    @declared_attr
    def validated_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def validated_by(cls):
        return relationship("User", foreign_keys=[cls.validated_by_id])

class Exploration(Job):
    
    __tablename__ = 'job_exploration'
    
    id = Column(String(36), ForeignKey('jobs.id'), primary_key=True)

    well_id = Column(String(36), ForeignKey('wells.id'))

    well = relationship('Well', foreign_keys=[well_id])

    __mapper_args__ = {
        "polymorphic_identity": "exploration",
    }

class Development(Job):
    
    __tablename__ = 'job_development'
    
    id = Column(String(36), ForeignKey('jobs.id'), primary_key=True)
    
    well_id = Column(String(36), ForeignKey('wells.id'))

    well = relationship('Well', foreign_keys=[well_id])

    __mapper_args__ = {
        "polymorphic_identity": "development",
    }

class Workover(Job):
    
    __tablename__ = 'job_workover'
    
    id = Column(String(36), ForeignKey('jobs.id'), primary_key=True)
    
    well_id = Column(Integer, ForeignKey('wells.id'))
    well = relationship('Well', foreign_keys=[well_id])
    
    job_category = Column(Enum(WOWSJobType))
    
    #current
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    water_cut = Column(Float)
    
    __mapper_args__ = {
        "polymorphic_identity": "workover",
    }

class WellService(Job):
    
    __tablename__ = 'job_well_service'
    
    id = Column(String(36), ForeignKey('jobs.id'), primary_key=True)
    
    well_id = Column(Integer, ForeignKey('wells.id'))
    well = relationship('Well', foreign_keys=[well_id])
    
    job_category = Column(Enum(WOWSJobType))
    
    #current
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    water_cut = Column(Float)
    
    __mapper_args__ = {
        "polymorphic_identity": "wellservice",
    }

class PlanningStatus(PyEnum):
    PROPOSED = 'PROPOSED'
    APPROVED = 'APPROVED'
    RETURNED = 'RETURNED'

class OperationStatus(PyEnum):
    OPERATING = 'OPERATING'
    FINISHED = 'FINISHED'

class PPPStatus(PyEnum):
    PROPOSED = 'PROPOSED'
    APPROVED = 'APPROVED'

class CloseOutStatus(PyEnum):
    PROPOSED = 'PROPOSED'
    APPROVED = 'APPROVED'

class Planning(Base, CreateBase, EditBase, ValidationBase):

    __tablename__ = 'job_plans'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    proposed_job_id = Column(String(36), ForeignKey('jobs.id'))
    proposed_job = relationship('Job', foreign_keys=[proposed_job_id])

    approved_job_id = Column(String(36), ForeignKey('jobs.id'))
    approved_job = relationship('Job', foreign_keys=[approved_job_id])
    
    date_proposed = Column(Date)
    date_returned = Column(Date)
    date_approved = Column(Date)
    
    status = Column(Enum(PlanningStatus))
    
class JobIssue(Base):
    
    __tablename__ = 'job_issues'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_operation_id = Column(String(36), ForeignKey('job_operations.id'))
    job_operation = relationship('Operation', back_populates='job_issues')
    
    date_time = Column(DateTime)
    severity = Column(Enum(Severity))
    description = Column(Text)
    
    resolved = Column(Boolean)
    resolved_date_time = Column(DateTime)

class Operation(Base, CreateBase, EditBase):
    
    __tablename__ = 'job_operations'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_plan_id = Column(String(36), ForeignKey('job_plans.id'))
    job_plan = relationship('Planning', foreign_keys=[job_plan_id])
    
    post_operation_job_id = Column(String(36), ForeignKey('jobs.id'))
    post_operation_job = relationship('Job', foreign_keys=[post_operation_job_id])
    
    date_started = Column(Date)
    date_finished = Column(Date)
    
    job_issues = relationship('JobIssue', back_populates='job_operation')
    
    status = Column(Enum(OperationStatus))

class PPP(Base, CreateBase, EditBase, ValidationBase):

    __tablename__ = 'job_ppp'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_operation_id = Column(String(36), ForeignKey('job_operations.id'))
    job_operation = relationship('Operation', foreign_keys=[job_operation_id])

    approved_job_id = Column(String(36), ForeignKey('jobs.id'))
    approved_job = relationship('Job', foreign_keys=[approved_job_id])
    
    date_proposed = Column(Date)
    date_approved = Column(Date)
    
    status = Column(Enum(PPPStatus))

class CloseOut(Base, CreateBase, EditBase, ValidationBase):

    __tablename__ = 'job_closeout'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_ppp_id = Column(String(36), ForeignKey('job_ppp.id'))
    job_ppp = relationship('PPP', foreign_keys=[job_ppp_id])
    
    date_proposed = Column(Date)
    date_approved = Column(Date)
    
    status = Column(Enum(CloseOutStatus))

