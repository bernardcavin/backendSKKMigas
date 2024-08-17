from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float, Table
from enum import Enum as PyEnum
from app.database import Base
import uuid

class DataPhase(PyEnum):
    PLAN = 'PLAN'
    ACTUAL = 'ACTUAL'

class Severity(PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CreateEditBase:
    
    date_created = Column(DateTime)
    last_edited = Column(DateTime)
    
    @declared_attr
    def created_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])

    @declared_attr
    def last_edited_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class TahapanBase(CreateEditBase):
    
    @declared_attr
    def job_id(cls):
        return Column(String(36), ForeignKey('jobs.id'))

    @declared_attr
    def job(cls):
        return relationship("Job", foreign_keys=[cls.job_id])

    @declared_attr
    def issue_id(cls):
        return Column(String(36), ForeignKey('job_issues.id'))

    @declared_attr
    def issue(cls):
        return relationship("Issue", foreign_keys=[cls.issue_id])

class Issue(Base,CreateEditBase):
    
    __tablename__ = 'job_issues'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    date_time = Column(DateTime)
    severity = Column(Enum(Severity))
    description = Column(Text)
    
    resolved = Column(Boolean)
    resolved_date_time = Column(DateTime)

class ValidationBase:
    @declared_attr
    def validated_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def validated_by(cls):
        return relationship("User", foreign_keys=[cls.validated_by_id])
    
    @declared_attr
    def validation_date(cls):
        return Column(DateTime)

class StatusPengajuan(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class Pengajuan(Base,TahapanBase, ValidationBase):

    __tablename__ = 'job_pengajuan'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', foreign_keys=[job_id])
    
    tanggal_diajukan = Column(DateTime)
    tanggal_ditolak = Column(DateTime)
    tanggal_disetujui = Column(DateTime)
    
    status = Column(Enum(StatusPengajuan))

class StatusOperasi(PyEnum):
    BEROPERASI = 'BEROPERASI'
    TERKENDALA = 'TERKENDALA'
    SELESAI = 'SELESAI'

class Operasi(Base,TahapanBase, ValidationBase):

    __tablename__ = 'job_operasi'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    tahap_pengajuan_id =Column(String(36), ForeignKey('job_pengajuan.id'))
    tahap_pengajuan = relationship('Pengajuan', foreign_keys=[tahap_pengajuan_id])
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusPPP(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class PPP(Base,TahapanBase, ValidationBase):

    __tablename__ = 'job_ppp'

    id = Column(String, primary_key=True)
    tahap_operasi_id =Column(String(36), ForeignKey('job_operasi.id'))
    tahap_operasi = relationship('Operasi', foreign_keys=[tahap_operasi_id])
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusCloseOut(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class CloseOut(Base,TahapanBase, ValidationBase):

    __tablename__ = 'job_closeout'

    id = Column(String, primary_key=True)
    
    tahap_ppp_id =Column(String(36), ForeignKey('job_ppp.id'))
    tahap_ppp = relationship('PPP', foreign_keys=[tahap_ppp_id])
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class JobType(PyEnum):
    DRILLING = 'DRILLING'
    WOWS = 'WOWS'

class ContractType(PyEnum):
    COST_RECOVERY = 'COST-RECOVERY'
    GROSS_SPLIT = 'GROSS-SPLIT'

class RigType(PyEnum):
    JACK_UP = 'JACK-UP'
    BARGE = 'BARGE'
    FLOATER = 'FLOATER'
    SEMI_SUBMERSIBLE = 'SEMI-SUBMERSIBLE'
    DRILLSHIP = 'DRILLSHIP'

class Job(Base, CreateEditBase):

    __tablename__ = 'jobs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    #kkks information
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship('KKKS', back_populates='jobs')
    
    field_id = Column(String(36), ForeignKey('fields.id'))
    field = relationship('Field', back_populates='jobs')
    
    #contract information
    contract_type = Column(Enum(ContractType))
    job_type = Column(Enum(JobType))
    
    afe_number = Column(String)
    wpb_year = Column(Integer)
    
    #plan
    plan_start = Column(DateTime)
    plan_end = Column(DateTime)
    plan_total_budget = Column(Numeric(precision=10, scale=2))
    
    #actual
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    actual_total_budget = Column(Numeric(precision=10, scale=2))
    
    #rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    #job activity
    job_activity = relationship('JobActivity', back_populates='job')
    budget = relationship('Budget', back_populates='job')
    work_breakdown_structure = relationship('WorkBreakdownStructure', back_populates='job')
    drilling_hazard = relationship('DrillingHazard', back_populates='job')
    job_documents = relationship('JobDocument', back_populates='job')
        
    __mapper_args__ = {
        'polymorphic_identity': 'jobs',
        'polymorphic_on': job_type
    }

class WorkBreakdownStructure(Base):
    
    __tablename__ = 'job_wbs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='work_breakdown_structure')
    
    data_phase = Column(Enum(DataPhase))
    
    event = Column(String)
    start_date = Column(DateTime)
    end_data = Column(DateTime)
    remarks = Column(Text)

class HazardType(PyEnum):
    GAS_KICK = "GAS KICK"
    STUCK_PIPE = "STUCK PIPE"
    LOST_CIRCULATION = "LOST CIRCULATION"
    WELL_CONTROL = "WELL CONTROL"
    EQUIPMENT_FAILURE = "EQUIPMENT FAILURE"
    OTHER = "OTHER"

class Budget(Base):
    
    __tablename__ = 'job_budget'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='budget')
    
    data_phase = Column(Enum(DataPhase))

    tangible_cost = Column(Numeric(precision=10, scale=2))
    intangible_cost = Column(Numeric(precision=10, scale=2))
    total_cost = Column(Numeric(precision=10, scale=2))

class DrillingHazard(Base):
    
    __tablename__ = 'job_drilling_hazard'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='drilling_hazard')
    
    data_phase = Column(Enum(DataPhase))
    
    hazard_type = Column(Enum(HazardType))
    hazard_description = Column(Text)
    severity = Column(Enum(Severity))
    mitigation = Column(Text)
    
    remark = Column(Text)

from app.routers.well.models import DepthUOM, DepthDatum, MediaType, SizeUOM

class JobDocument(Base):
    
    __tablename__ = 'job_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_documents')
    
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

class JobActivity(Base):
    
    __tablename__ = 'job_activity'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    data_phase = Column(Enum(DataPhase))

    time = Column(DateTime)
    
    measured_depth = Column(Float)
    measured_depth_uoum = Column(Enum(DepthUOM))
    measured_depth_datum = Column(Enum(DepthDatum))
    
    true_vertical_depth = Column(Float)
    true_vertical_depth_uoum = Column(Enum(DepthUOM))
    
    true_vertical_depth_sub_sea = Column(Float)
    true_vertical_depth_sub_sea_uoum = Column(Enum(DepthUOM))
    
    daily_cost = Column(Numeric(precision=10, scale=2))
    
    summary = Column(Text)
    current_operations = Column(Text)
    next_operations = Column(Text)
    
    job_id = Column(String, ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_activity')

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
    
class DrillingClass(PyEnum):
    EXPLORATION = 'EXPLORATION'
    DEVELOPMENT = 'DEVELOPMENT'

class WOWSClass(PyEnum):
    WORKOVER = 'WORKOVER'
    WELLSERVICE = 'WELLSERVICE'

class Drilling(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.DRILLING
    }
    
    drilling_class = Column(Enum(DrillingClass))
    
    planned_well_id = Column(String(36), ForeignKey('wells.id'))
    final_well_id = Column(String(36), ForeignKey('wells.id'))

    planned_well = relationship('Well', foreign_keys=[planned_well_id])
    final_well = relationship('Well', foreign_keys=[final_well_id])
    
class WOWS(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.WOWS
    }
    
    wows_class = Column(Enum(WOWSClass))
    
    well_id = Column(Integer, ForeignKey('wells.id'))
    well = relationship('Well', foreign_keys=[well_id])
    job_category = Column(Enum(WOWSJobType))
    
    #current
    current_oil = Column(Float)
    current_gas = Column(Float)
    current_condensate = Column(Float)
    
    current_oil_water_cut = Column(Float)
    current_gas_water_cut = Column(Float)
    current_condensate_water_cut = Column(Float)
    
    #target
    target_oil = Column(Float)
    target_gas = Column(Float)
    target_condensate = Column(Float)
    
    target_oil_water_cut = Column(Float)
    target_gas_water_cut = Column(Float)
    target_condensate_water_cut = Column(Float)
    
    #final
    final_oil = Column(Float)
    final_gas = Column(Float)
    final_condensate = Column(Float)
    
    final_oil_water_cut = Column(Float)
    final_gas_water_cut = Column(Float)
    final_condensate_water_cut = Column(Float)