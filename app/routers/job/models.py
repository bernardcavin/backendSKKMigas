from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean, Float, Table
from enum import Enum as PyEnum
from app.database import Base
import uuid

class DataPhase(PyEnum):
    PLAN = 'PLAN'
    ACTUAL = 'ACTUAL'

class TahapanBase(Base):
    __abstract__ = True
    
    @declared_attr
    def pekerjaan_id(cls):
        return Column(String, ForeignKey('pekerjaan.id'))
    
    @declared_attr
    def pekerjaan(cls):
        return relationship("Pekerjaan", foreign_keys=[cls.pekerjaan_id])
    
    @declared_attr
    def kendala_id(cls):
        return Column(String, ForeignKey('kendala.id'))
    
    @declared_attr
    def kendala(cls):
        return relationship("Kendala", foreign_keys=[cls.kendala_id])
    
    @declared_attr
    def pekerjaan_id(cls):
        return Column(String, ForeignKey('pekerjaan.id'))
    
    @declared_attr
    def pekerjaan(cls):
        return relationship("Pekerjaan", foreign_keys=[cls.pekerjaan_id])
    
    @declared_attr
    def created_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class KategoriKendala(PyEnum):
    RINGAN = 'RINGAN'
    SEDANG = 'SEDANG'
    BERAT = 'BERAT'

class Kendala(Base):
    
    __tablename__ = 'kendala'
    
    id = Column(String, primary_key=True)
    waktu = Column(DateTime)
    kategori = Column(Enum(KategoriKendala))
    deskripsi = Column(Text)
    
    selesai = Column(Boolean)
    waktu_selesai = Column(DateTime)

class StatusPengajuan(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class Pengajuan(TahapanBase):

    __tablename__ = 'pengajuan'

    id = Column(String, primary_key=True)
    
    tanggal_diajukan = Column(DateTime)
    tanggal_ditolak = Column(DateTime)
    tanggal_disetujui = Column(DateTime)
    
    status = Column(Enum(StatusPengajuan))

class StatusOperasi(PyEnum):
    BEROPERASI = 'BEROPERASI'
    TERKENDALA = 'TERKENDALA'
    SELESAI = 'SELESAI'

class Operasi(TahapanBase):

    __tablename__ = 'operasi'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusPPP(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class PPP(TahapanBase):

    __tablename__ = 'ppp'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusCloseOut(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class CloseOut(TahapanBase):

    __tablename__ = 'closeout'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class JobType(PyEnum):
    EKSPLORASI = 'EKSPLORASI'
    EKSPLOITASI = 'EKSPLOITASI'
    WORKOVER = 'WORKOVER'
    WELLSERVICE = 'WELSERVICE'


class ContractType(PyEnum):
    COST_RECOVERY = 'COST_RECOVERY'
    GROSS_SPLIT = 'GROSS_SPLIT'

class RigType(PyEnum):
    JACK_UP = 'JACK-UP'
    BARGE = 'BARGE'
    FLOATER = 'FLOATER'
    SEMI_SUBMERSIBLE = 'SEMI-SUBMERSIBLE'
    DRILLSHIP = 'DRILLSHIP'

class Job(Base):

    __tablename__ = 'jobs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    #well
    well_id = Column(String(36), ForeignKey('wells.id'))
    well = relationship("Job", back_populates="jobs")
    
    #kkks information
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    last_edited_by = relationship("KKKS", foreign_keys=[kkks_id])
    
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
    
    #other
    date_created = Column(DateTime)
    last_edited = Column(DateTime)

    created_by_id = Column(Integer,ForeignKey('users.id'))
    last_edited_by_id = Column(Integer, ForeignKey('users.id'))
    last_edited_by = relationship("User", foreign_keys=[last_edited_by_id])
    last_edited_by = relationship("User", foreign_keys=[created_by_id])
    
    __mapper_args__ = {
        'polymorphic_identity': 'jobs',
        'polymorphic_on': job_type
    }


from app.routers.well.models import DepthUOM, DepthDatum

class JobActivity(Base):
    
    __tablename__ = 'job_activity'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

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

class Eksplorasi(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.EKSPLORASI
    }
    


class Eksploitasi(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.EKSPLOITASI
    }

class Workover(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.WORKOVER
    }

class WellService(Job):
    __mapper_args__ = {
        'polymorphic_identity': JobType.WELLSERVICE
    }

class WorkBreakdownStructure(Base):
    
    __tablename__ = 'wbs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    
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

class Severity(PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DrillingHazard(Base):
    
    __tablename__ = 'drilling_hazard'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'))
    
    data_phase = Column(Enum(DataPhase))
    
    hazard_type = Column(Enum(HazardType))
    hazard_description = Column(Text)
    severity = Column(Enum(Severity))
    mitigation = Column(Text)
    
    remark = Column(Text)



