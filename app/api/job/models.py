from os import close
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, Enum, Text, Boolean, Float, Date, func, select, case, and_
from app.api.well.models import ActualWell, DepthDatum, PlanWell, WellInstance
from sqlalchemy.orm import relationship, declared_attr, with_polymorphic, aliased
from app.core.database import Base
from enum import Enum as PyEnum
import uuid
from app.core.enum_operations import extend_enum
from app.core.constants import uom, UnitType
from sqlalchemy.ext.hybrid import hybrid_property
from app.api.spatial.models import Area,Lapangan
from app.api.auth.models import KKKS
from typing import List
from datetime import datetime, timedelta

class Percentage(PyEnum):
    P0 = "0%"
    P5 = "5%"
    P10 = "10%"
    P15 = "15%"
    P20 = "20%"
    P25 = "25%"
    P30 = "30%"
    P35 = "35%"
    P40 = "40%"
    P45 = "45%"
    P50 = "50%"
    P55 = "55%"
    P60 = "60%"
    P65 = "65%"
    P70 = "70%"
    P75 = "75%"
    P80 = "80%"
    P85 = "85%"
    P90 = "90%"
    P95 = "95%"
    P100 = "100%"

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
    PROPOSED = 'PROPOSED'
    APPROVED = 'APPROVED'
    RETURNED = 'RETURNED'
    POST_OPERATION = 'POST OPERATION'
    PPP = 'PPP'

class HazardType(PyEnum):
    GAS_KICK = "GAS KICK"
    STUCK_PIPE = "STUCK PIPE"
    LOST_CIRCULATION = "LOST CIRCULATION"
    WELL_CONTROL = "WELL CONTROL"
    EQUIPMENT_FAILURE = "EQUIPMENT FAILURE"
    OTHER = "OTHER"

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

class JobType(PyEnum):
    EXPLORATION = 'EXPLORATION'
    DEVELOPMENT = 'DEVELOPMENT'
    WORKOVER = 'WORKOVER'
    WELLSERVICE = 'WELLSERVICE'
    
class ValidationBase:
    
    remarks = Column(Text)
    
    @declared_attr
    def approved_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def approved_by(cls):
        return relationship("User", foreign_keys=[cls.approved_by_id])
    
    @declared_attr
    def returned_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def returned_by(cls):
        return relationship("User", foreign_keys=[cls.returned_by_id])

class CreateBase:
    
    time_created = Column(DateTime, default=func.now())
    
    @declared_attr
    def created_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))

    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])

class EditBase:
    
    last_edited = Column(DateTime, onupdate=func.now())
    
    @declared_attr
    def last_edited_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class Job(Base, CreateBase, ValidationBase, EditBase):
    
    __tablename__ = 'jobs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    job_type = Column(Enum(JobType))
    
    #kkks information
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship('KKKS', back_populates='jobs')
    
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship('Area', back_populates='jobs')
    
    field_id = Column(String(36), ForeignKey('fields.id'))
    field = relationship('Lapangan', back_populates='jobs')
    
    @hybrid_property
    def kkks_name(self):
        return self.kkks.name if self.kkks else None
    
    @kkks_name.expression
    def kkks_name(cls):
        return select(KKKS.name).where(cls.kkks_id == KKKS.id).as_scalar()

    @hybrid_property
    def area_name(self):
        return self.area.name if self.area else None
    
    @area_name.expression
    def area_name(cls):
        return select(Area.name).where(cls.area_id == Area.id).as_scalar()

    @hybrid_property
    def region(self):
        return self.area.region if self.area else None
    
    @region.expression
    def region(cls):
        return select(Area.region).where(cls.area_id == Area.id).as_scalar()

    @hybrid_property
    def field_name(self):
        return self.field.name if self.field else None
    
    @field_name.expression
    def field_name(cls):
        return select(Lapangan.name).where(cls.field_id == Lapangan.id).as_scalar()
    
    #contract information
    contract_type = Column(Enum(ContractType))
    
    afe_number = Column(String(20))
    wpb_year = Column(Integer)
    
    #Planning
    job_plan_id = Column(String(36), ForeignKey('job_instances.job_instance_id'))
    job_plan = relationship('JobInstance', foreign_keys=[job_plan_id])
    
    @property
    def well_name(self):
        if self.job_type in [JobType.WORKOVER,JobType.WELLSERVICE]:
            return self.job_plan.well.well_name if self.job_plan else None
        else:
            return self.job_plan.well.well_name if self.job_plan else None

    date_proposed = Column(Date)
    date_returned = Column(Date)
    date_approved = Column(Date)
    
    planning_status = Column(Enum(PlanningStatus))
    
    #Operation
    actual_job_id = Column(String(36), ForeignKey('job_instances.job_instance_id'))
    actual_job = relationship('JobInstance', foreign_keys=[actual_job_id])
    
    daily_operations_report = relationship('DailyOperationsReport', back_populates='job')
    
    @hybrid_property
    def plan_start_date(self):
        return self.job_plan.start_date if self.job_plan else None
    
    @plan_start_date.expression
    def plan_start_date(cls):
        return select(JobInstance.start_date).where(cls.job_plan_id == JobInstance.job_instance_id).as_scalar()

    @hybrid_property
    def plan_total_budget(self):
        return self.job_plan.total_budget if self.job_plan else None
    
    @plan_total_budget.expression
    def plan_total_budget(cls):
        return select(JobInstance.total_budget).where(cls.job_plan_id == JobInstance.job_instance_id).as_scalar()
    
    @hybrid_property
    def plan_end_date(self):
        return self.job_plan.end_date if self.job_plan else None
    
    @plan_end_date.expression
    def plan_end_date(cls):
        return select(JobInstance.end_date).where(cls.job_plan_id == JobInstance.job_instance_id).as_scalar()

    @hybrid_property
    def actual_start_date(self):
        return self.actual_job.start_date if self.actual_job else None
    
    @actual_start_date.expression
    def actual_start_date(cls):
        return select(JobInstance.start_date).where(cls.actual_job_id == JobInstance.job_instance_id).as_scalar()

    @hybrid_property
    def actual_total_budget(self):
        return self.actual_job.total_budget if self.actual_job else None
    
    @actual_total_budget.expression
    def actual_total_budget(cls):
        return select(JobInstance.total_budget).where(cls.actual_job_id == JobInstance.job_instance_id).as_scalar()

    @hybrid_property
    def actual_end_date(self):
        return self.actual_job.end_date if self.actual_job else None
    
    @actual_end_date.expression
    def actual_end_date(cls):
        return select(JobInstance.end_date).where(cls.actual_job_id == JobInstance.job_instance_id).as_scalar()
        
    job_issues = relationship('JobIssue', back_populates='job')
    operation_status = Column(Enum(OperationStatus))
    
    #PPP
    date_ppp_proposed = Column(Date)
    
    #syarat PPP
    surat_pengajuan_ppp_id = Column(String(36), ForeignKey('job_documents.id'))
    nomor_surat_pengajuan_ppp = Column(String(50))
    surat_pengajuan_ppp = relationship('JobDocument', foreign_keys=[surat_pengajuan_ppp_id])
    surat_pengajuan_ppp_approval = Column(Boolean)
    
    # Field for Dokumen Persetujuan AFE/WP&B
    dokumen_persetujuan_afe_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_persetujuan_afe = relationship('JobDocument', foreign_keys=[dokumen_persetujuan_afe_id])
    surat_pengajuan_persetujuan_afe_approval = Column(Boolean, default=False)

    # Field for Dokumen Project Summary
    dokumen_project_summary_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_project_summary = relationship('JobDocument', foreign_keys=[dokumen_project_summary_id])
    surat_pengajuan_project_summary_approval = Column(Boolean, default=False)

    # Field for Dokumen Pernyataan
    dokumen_pernyataan_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_pernyataan = relationship('JobDocument', foreign_keys=[dokumen_pernyataan_id])
    surat_pengajuan_pernyataan_approval = Column(Boolean, default=False)

    # Field for Dokumen Laporan Pekerjaan
    dokumen_laporan_pekerjaan_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_laporan_pekerjaan = relationship('JobDocument', foreign_keys=[dokumen_laporan_pekerjaan_id])
    surat_pengajuan_laporan_pekerjaan_approval = Column(Boolean, default=False)

    # Field for Dokumen Formulir
    dokumen_formulir_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_formulir = relationship('JobDocument', foreign_keys=[dokumen_formulir_id])
    surat_pengajuan_formulir_approval = Column(Boolean, default=False)

    # Field for Dokumen Korespondensi
    dokumen_korespondensi_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_korespondensi = relationship('JobDocument', foreign_keys=[dokumen_korespondensi_id])
    surat_pengajuan_korespondensi_approval = Column(Boolean, default=False)

    # Field for Dokumen Sumur Tidak Berproduksi
    dokumen_sumur_tidak_berproduksi_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_sumur_tidak_berproduksi = relationship('JobDocument', foreign_keys=[dokumen_sumur_tidak_berproduksi_id])
    surat_pengajuan_sumur_tidak_berproduksi_approval = Column(Boolean, default=False)

    # Field for Dokumen Daftar Material
    dokumen_daftar_material_id = Column(String(36), ForeignKey('job_documents.id'))
    dokumen_daftar_material = relationship('JobDocument', foreign_keys=[dokumen_daftar_material_id])
    surat_pengajuan_daftar_material_approval = Column(Boolean, default=False)
    
    date_ppp_approved = Column(Date)
    
    ppp_status = Column(Enum(PPPStatus))
    
    #CloseOut
    date_co_proposed = Column(Date)
    date_co_approved = Column(Date)
    
    closeout_status = Column(Enum(CloseOutStatus))

    # @hybrid_property
    # def job_current_status(self):
    #     if self.closeout_status is not None:
    #         return self.closeout_status
    #     elif self.ppp_status is not None:
    #         return self.ppp_status
    #     elif self.operation_status is not None:
    #         return self.operation_status
    #     else:
    #         return self.planning_status

    # @job_current_status.expression
    # def job_current_status(cls):
    #     return case(
            
    #         (
    #             and_(
    #                 cls.closeout_status.is_(None),
    #                 cls.ppp_status.is_(None),
    #                 cls.operation_status.is_(None),
    #                 cls.planning_status.isnot(None),
    #             ),
    #             cls.planning_status
    #         ),
    #         # (
    #         #     and_(
    #         #         cls.closeout_status.is_(None),
    #         #         cls.ppp_status.is_(None),
    #         #         cls.operation_status.isnot(None),
    #         #         cls.planning_status.isnot(None),
    #         #     ),
    #         #     cls.operation_status
    #         # ),
    #         # (
    #         #     and_(
    #         #         cls.closeout_status.is_(None),
    #         #         cls.ppp_status.isnot(None),
    #         #         cls.operation_status.isnot(None),
    #         #         cls.planning_status.isnot(None),
    #         #     ),
    #         #     cls.ppp_status
    #         # ),
    #         # (
    #         #     and_(
    #         #         cls.closeout_status.isnot(None),
    #         #         cls.ppp_status.isnot(None),
    #         #         cls.operation_status.isnot(None),
    #         #         cls.planning_status.isnot(None),
    #         #     ),
    #         #     cls.closeout_status
    #         # )
    #     )
        
    
    @property
    def job_current_status(self):
        if self.closeout_status is not None:
            return self.closeout_status
        elif self.ppp_status is not None:
            return self.ppp_status
        elif self.operation_status is not None:
            return self.operation_status
        else:
            return self.planning_status
    
class JobInstance(Base):
    
    __tablename__ = 'job_instances'
    
    job_instance_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    well_id = Column(String(36), ForeignKey('well_instances.well_instance_id'))
    
    job_phase_type = Column(String(20))
    
    start_date = Column(Date)
    end_date = Column(Date)
    total_budget = Column(Numeric(precision=10, scale=2))
    
    job_operation_days = relationship('JobOperationDay', back_populates='job_instance')
    
    job_hazards = relationship('JobHazard', back_populates='job_instance')
    job_documents = relationship('JobDocument', back_populates='job_instance')
    
    work_breakdown_structure_id = Column(String(36), ForeignKey('job_wbs.id'))
    work_breakdown_structure = relationship('WorkBreakdownStructure', foreign_keys=[work_breakdown_structure_id])
    
    __mapper_args__ = {
        "polymorphic_on": "job_phase_type",
    }
    
    # def get_job_date_list(self) -> List[str]:
    #     """
    #     Generate a list of dates for the job instance.
        
    #     :return: A list of date strings in 'YYYY-MM-DD' format
    #     """
    #     if self.start_date and self.end_date:
    #         return generate_date_list(self.start_date, self.end_date)
    #     return []

# def generate_date_list(start_date: datetime, end_date: datetime) -> List[str]:
#     """
#     Generate a list of dates between start_date and end_date (inclusive).
    
#     :param start_date: The start date
#     :param end_date: The end date
#     :return: A list of date strings in 'YYYY-MM-DD' format
#     """
#     date_list = []
#     current_date = start_date
#     while current_date <= end_date:
#         date_list.append(current_date.strftime('%Y-%m-%d'))
#         current_date += timedelta(days=1)
#     return date_list

class PlanExploration(JobInstance):
    
    __tablename__ = 'job_plan_exploration'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('PlanWell', foreign_keys=[JobInstance.well_id])
    
    # rig information
    rig_name = Column(String(50))
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    wrm_pembebasan_lahan = Column(Boolean)
    wrm_ippkh = Column(Boolean)
    wrm_ukl_upl = Column(Boolean)
    wrm_amdal = Column(Boolean)
    wrm_pengadaan_rig = Column(Boolean)
    wrm_pengadaan_drilling_services = Column(Boolean)
    wrm_pengadaan_lli = Column(Boolean)
    wrm_persiapan_lokasi = Column(Boolean)
    wrm_internal_kkks = Column(Boolean)
    wrm_evaluasi_subsurface = Column(Boolean)

    __mapper_args__ = {
        "polymorphic_identity": 'plan_exploration',
    }

class PlanDevelopment(JobInstance):
    
    __tablename__ = 'job_plan_development'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('PlanWell', foreign_keys=[JobInstance.well_id])

    # rig information
    rig_name = Column(String(50))
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)
   
    wrm_pembebasan_lahan = Column(Boolean)
    wrm_ippkh = Column(Boolean)
    wrm_ukl_upl = Column(Boolean)
    wrm_amdal = Column(Boolean)
    wrm_cutting_dumping = Column(Boolean)
    wrm_pengadaan_rig = Column(Boolean)
    wrm_pengadaan_drilling_services = Column(Boolean)
    wrm_pengadaan_lli = Column(Boolean)
    wrm_persiapan_lokasi = Column(Boolean)
    wrm_internal_kkks = Column(Boolean)
    wrm_evaluasi_subsurface = Column(Boolean)

    __mapper_args__ = {
        "polymorphic_identity": 'plan_development',
    }

class PlanWorkover(JobInstance):
    
    __tablename__ = 'job_plan_workover'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])
    
    equipment = Column(String(50))
    equipment_specifications = Column(Text)
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    #current
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    #target
    target_oil = Column(Float)
    target_gas = Column(Float)
    target_water_cut = Column(Float)

    wrm_internal_kkks = Column(Boolean)
    wrm_pengadaan_equipment = Column(Boolean)
    wrm_pengadaan_services = Column(Boolean)
    wrm_pengadaan_handak = Column(Boolean)
    wrm_pengadaan_octg = Column(Boolean)
    wrm_pengadaan_lli = Column(Boolean)
    wrm_pengadaan_artificial_lift = Column(Boolean)
    wrm_sumur_berproduksi = Column(Boolean)
    wrm_fasilitas_produksi = Column(Boolean)
    wrm_persiapan_lokasi = Column(Boolean)
    wrm_well_integrity = Column(Boolean)

    #well schematic
    well_schematic_id = Column(String(36), ForeignKey('job_well_schematics.id'))
    well_schematic = relationship('WellSchematic', foreign_keys=[well_schematic_id])
    
    __mapper_args__ = {
        "polymorphic_identity": 'plan_workover',
    }

class PlanWellService(JobInstance):
    
    __tablename__ = 'job_plan_well_service'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])
    
    equipment = Column(String(50))
    equipment_specifications = Column(Text)
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    #current
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    #target
    target_oil = Column(Float)
    target_gas = Column(Float)
    target_water_cut = Column(Float)
    
    wrm_internal_kkks = Column(Boolean)
    wrm_pengadaan_equipment = Column(Boolean)
    wrm_pengadaan_services = Column(Boolean)
    wrm_pengadaan_handak = Column(Boolean)
    wrm_pengadaan_octg = Column(Boolean)
    wrm_pengadaan_lli = Column(Boolean)
    wrm_pengadaan_artificial_lift = Column(Boolean)
    wrm_sumur_berproduksi = Column(Boolean)
    wrm_fasilitas_produksi = Column(Boolean)
    wrm_persiapan_lokasi = Column(Boolean)
    wrm_well_integrity = Column(Boolean)

    #well schematic
    well_schematic_id = Column(String(36), ForeignKey('job_well_schematics.id'))
    well_schematic = relationship('WellSchematic', foreign_keys=[well_schematic_id])
        
    __mapper_args__ = {
        "polymorphic_identity": 'plan_wellservice',
    }

class ActualExploration(JobInstance):
    
    __tablename__ = 'job_actual_exploration'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])
    
    # rig information
    rig_name = Column(String(50))
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    wrm_pembebasan_lahan = Column(Enum(Percentage))
    wrm_ippkh = Column(Enum(Percentage))
    wrm_ukl_upl = Column(Enum(Percentage))
    wrm_amdal = Column(Enum(Percentage))
    wrm_pengadaan_rig = Column(Enum(Percentage))
    wrm_pengadaan_drilling_services = Column(Enum(Percentage))
    wrm_pengadaan_lli = Column(Enum(Percentage))
    wrm_persiapan_lokasi = Column(Enum(Percentage))
    wrm_internal_kkks = Column(Enum(Percentage))
    wrm_evaluasi_subsurface = Column(Enum(Percentage))

    __mapper_args__ = {
        "polymorphic_identity": 'actual_exploration',
    }

class ActualDevelopment(JobInstance):
    
    __tablename__ = 'job_actual_development'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])

    # rig information
    rig_name = Column(String(50))
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)
    
    wrm_pembebasan_lahan = Column(Enum(Percentage))
    wrm_ippkh = Column(Enum(Percentage))
    wrm_ukl_upl = Column(Enum(Percentage))
    wrm_amdal = Column(Enum(Percentage))
    wrm_cutting_dumping = Column(Enum(Percentage))
    wrm_pengadaan_rig = Column(Enum(Percentage))
    wrm_pengadaan_drilling_services = Column(Enum(Percentage))
    wrm_pengadaan_lli = Column(Enum(Percentage))
    wrm_persiapan_lokasi = Column(Enum(Percentage))
    wrm_internal_kkks = Column(Enum(Percentage))
    wrm_evaluasi_subsurface = Column(Enum(Percentage))

    __mapper_args__ = {
        "polymorphic_identity": 'actual_development',
    }

class ActualWorkover(JobInstance):
    
    __tablename__ = 'job_actual_workover'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])
    
    equipment = Column(String(50))
    equipment_specifications = Column(Text)
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    #target
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    wrm_internal_kkks = Column(Enum(Percentage))
    wrm_pengadaan_equipment = Column(Enum(Percentage))
    wrm_pengadaan_services = Column(Enum(Percentage))
    wrm_pengadaan_handak = Column(Enum(Percentage))
    wrm_pengadaan_octg = Column(Enum(Percentage))
    wrm_pengadaan_lli = Column(Enum(Percentage))
    wrm_pengadaan_artificial_lift = Column(Enum(Percentage))
    wrm_sumur_berproduksi = Column(Enum(Percentage))
    wrm_fasilitas_produksi = Column(Enum(Percentage))
    wrm_persiapan_lokasi = Column(Enum(Percentage))
    wrm_well_integrity = Column(Enum(Percentage))
    
    #well schematic
    well_schematic_id = Column(String(36), ForeignKey('job_well_schematics.id'))
    well_schematic = relationship('WellSchematic', foreign_keys=[well_schematic_id])
    
    # #completion string
    # completion_id = Column(String(36), ForeignKey('job_workover_completion_actuals.id'))
    # completion = relationship('ActualWorkoverCompletion', foreign_keys=[completion_id])
    
    __mapper_args__ = {
        "polymorphic_identity": 'actual_workover',
    }

class ActualWellService(JobInstance):
    
    __tablename__ = 'job_actual_well_service'
    
    id = Column(String(36), ForeignKey('job_instances.job_instance_id'), primary_key=True)
    
    well = relationship('ActualWell', foreign_keys=[JobInstance.well_id])
    
    equipment = Column(String(50))
    equipment_specifications = Column(Text)
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    wrm_internal_kkks = Column(Enum(Percentage))
    wrm_pengadaan_equipment = Column(Enum(Percentage))
    wrm_pengadaan_services = Column(Enum(Percentage))
    wrm_pengadaan_handak = Column(Enum(Percentage))
    wrm_pengadaan_octg = Column(Enum(Percentage))
    wrm_pengadaan_lli = Column(Enum(Percentage))
    wrm_pengadaan_artificial_lift = Column(Enum(Percentage))
    wrm_sumur_berproduksi = Column(Enum(Percentage))
    wrm_fasilitas_produksi = Column(Enum(Percentage))
    wrm_persiapan_lokasi = Column(Enum(Percentage))
    wrm_well_integrity = Column(Enum(Percentage))
    
    #well schematic
    well_schematic_id = Column(String(36), ForeignKey('job_well_schematics.id'))
    well_schematic = relationship('WellSchematic', foreign_keys=[well_schematic_id])
    
    __mapper_args__ = {
        "polymorphic_identity": 'actual_wellservice',
    }

class WorkBreakdownStructure(Base):
    
    __tablename__ = 'job_wbs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    job_instance = relationship('JobInstance', back_populates='work_breakdown_structure', single_parent=True)
    
    wbs_type = Column(String(4))
    
    events = relationship('WBSCustomEvent', secondary='job_wbs_events_r')

    wrm_internal_kkks_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_internal_kkks = relationship('WBSWRMEvent', foreign_keys=[wrm_internal_kkks_id])

    wrm_persiapan_lokasi_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_persiapan_lokasi = relationship('WBSWRMEvent', foreign_keys=[wrm_persiapan_lokasi_id])

    wrm_pengadaan_lli_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_lli = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_lli_id])

    __mapper_args__ = {
        'polymorphic_identity': 'wrm_event',
        'polymorphic_on': wbs_type
    }

class WBSCustomEventRelationship(Base):
    __tablename__ = 'job_wbs_events_r'
    
    wbs_id = Column(String(36), ForeignKey('job_wbs.id'), primary_key=True)
    event_id = Column(String(36), ForeignKey('job_wbs_events.id'), primary_key=True)
    
class WorkBreakdownStructureDrilling(WorkBreakdownStructure):
    
    wrm_pembebasan_lahan_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pembebasan_lahan = relationship('WBSWRMEvent', foreign_keys=[wrm_pembebasan_lahan_id])
    
    wrm_ippkh_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_ippkh = relationship('WBSWRMEvent', foreign_keys=[wrm_ippkh_id])
    
    wrm_ukl_upl_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_ukl_upl = relationship('WBSWRMEvent', foreign_keys=[wrm_ukl_upl_id])
    
    wrm_amdal_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_amdal = relationship('WBSWRMEvent', foreign_keys=[wrm_amdal_id])
    
    wrm_pengadaan_rig_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_rig = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_rig_id])
    
    wrm_pengadaan_drilling_services_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_drilling_services = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_drilling_services_id])
    
    wrm_evaluasi_subsurface_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_evaluasi_subsurface = relationship('WBSWRMEvent', foreign_keys=[wrm_evaluasi_subsurface_id])
    
    wrm_cutting_dumping_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_cutting_dumping = relationship('WBSWRMEvent', foreign_keys=[wrm_cutting_dumping_id])

    __mapper_args__ = {
        'polymorphic_identity': 'drl',
    }

class WorkBreakdownStructureWOWS(WorkBreakdownStructure):
    
    wrm_pengadaan_equipment_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_equipment = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_equipment_id])
    
    wrm_pengadaan_services_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_services = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_services_id])
    
    wrm_pengadaan_handak_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_handak = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_handak_id])
    
    wrm_pengadaan_octg_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_octg = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_octg_id])
    
    wrm_pengadaan_artificial_lift_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_pengadaan_artificial_lift = relationship('WBSWRMEvent', foreign_keys=[wrm_pengadaan_artificial_lift_id])
    
    wrm_sumur_berproduksi_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_sumur_berproduksi = relationship('WBSWRMEvent', foreign_keys=[wrm_sumur_berproduksi_id])
    
    wrm_fasilitas_produksi_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_fasilitas_produksi = relationship('WBSWRMEvent', foreign_keys=[wrm_fasilitas_produksi_id])
    
    wrm_well_integrity_id = Column(String(36), ForeignKey('job_wbs_events.id'))
    wrm_well_integrity = relationship('WBSWRMEvent', foreign_keys=[wrm_well_integrity_id])
    
    __mapper_args__ = {
        'polymorphic_identity': 'wows',
    }

class WBSEvent(Base):
    
    __tablename__ = 'job_wbs_events'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    event_type = Column(String(12))
    start_date = Column(Date)
    end_date = Column(Date)
    remarks = Column(Text)
    
    __mapper_args__ = {
        'polymorphic_identity': 'event',
        'polymorphic_on': event_type
    }

class WBSWRMEvent(WBSEvent):

    __mapper_args__ = {
        'polymorphic_identity': 'wrm_event',
    }

class WBSCustomEvent(WBSEvent):
    
    event = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'custom_event',
    }

class JobHazard(Base):
    
    __tablename__ = 'job_hazards'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    job_instance_id = Column(String(36), ForeignKey('job_instances.job_instance_id'))
    job_instance = relationship('JobInstance', back_populates='job_hazards')
    
    hazard_type = Column(Enum(HazardType))
    hazard_description = Column(Text)
    severity = Column(Enum(Severity))
    mitigation = Column(Text)
    
    remark = Column(Text)

class JobDocumentType(PyEnum):
    DRILLING_PLAN = "Drilling Plan"
    COMPLETION_PLAN = "Completion Plan"
    WELL_DESIGN = "Well Design"
    MUD_PLAN = "Mud Plan"
    CEMENTING_PLAN = "Cementing Plan"
    WELL_TRAJECTORY_PLAN = "Well Trajectory Plan"
    RISK_ASSESSMENT_PLAN = "Risk Assessment Plan"
    SAFETY_PLAN = "Safety Plan"
    ENVIRONMENTAL_PLAN = "Environmental Plan"
    LOGGING_PLAN = "Logging Plan"
    PORE_PRESSURE_PREDICTION = "Pore Pressure Prediction"
    HYDRAULICS_PLAN = "Hydraulics Plan"
    CASING_PLAN = "Casing Plan"
    CONTINGENCY_PLAN = "Contingency Plan"
    SURAT_TAJAK = "Surat Tajak"
    PPP = "Dokumen Kelengkapan PPP"

class JobDocument(Base):
    
    __tablename__ = 'job_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    job_instance_id = Column(String(36), ForeignKey('job_instances.job_instance_id'))
    job_instance = relationship('JobInstance', back_populates='job_documents')

    file_id = Column(String(36), ForeignKey('files.id'))
    file = relationship('FileDB', foreign_keys=[file_id])
    
    document_type = Column(Enum(JobDocumentType))
    
    remark = Column(Text)
    
class JobOperationDay(Base):
    __tablename__ = 'job_operation_days'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    unit_type = Column(Enum(UnitType))

    phase = Column(String(50))
    
    depth_datum = Column(Enum(DepthDatum))
    
    depth_in = Column(Float)
    depth_out = Column(Float)
    depth_uom = Column(String(5))  # Changed to String
    
    operation_days = Column(Float)
    
    job_instance_id = Column(String(36), ForeignKey('job_instances.job_instance_id'))
    job_instance = relationship('JobInstance', back_populates='job_operation_days')

    def __init__(self, unit_type, *args, **kwargs):

        uom_map = uom.get(unit_type, {})
        self.depth_uom = uom_map.get('Length', 'm')  # Default to meters if not found
        self.unit_type = unit_type

        super().__init__(*args, **kwargs)

class JobIssue(Base):
    
    __tablename__ = 'job_issues'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_issues')
    
    date_time = Column(DateTime)
    severity = Column(Enum(Severity))
    description = Column(Text)
    
    resolved = Column(Boolean, default=False)
    resolved_date_time = Column(DateTime)

class YesNo(PyEnum):
    Y = 'Y'
    N = 'N'

class DailyOperationsReport(Base):
    
    __tablename__ = 'job_daily_operations_reports'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='daily_operations_report')
    
    #date
    report_date = Column(Date)
    
    #drilling parameters
    avg_wob = Column(Float)
    avg_rop = Column(Float)	
    avg_rpm = Column(Float)	
    torque = Column(Float)	
    stand_pipe_pressure = Column(Float)	
    flow_rate = Column(Float)	
    string_weight = Column(Float)	
    rotating_weight = Column(Float)	
    total_drilling_time = Column(Float)	
    circulating_pressure = Column(Float)	
    
    #afe
    daily_cost = Column(Float)
    daily_mud_cost = Column(Float)
    
    #human resource
    day_supervisor = Column(Float)
    night_supervisor =Column(Float)
    engineer = Column(Float)
    geologist = Column(Float)
    
    day_summary = Column(Text)
    day_forecast = Column(Text)
    
    #casing
    last_size = Column(Float)
    set_md = Column(Float)
    next_size = Column(Float)
    next_set_md = Column(Float)
    last_lot_emw = Column(Float)
    tol = Column(Float)
    
    #mud volumes
    start_mud_volume = Column(Float)
    lost_surface_mud_volume = Column(Float)
    lost_dh_mud_volume = Column(Float)
    dumped_mud_volume = Column(Float)
    built_mud_volume = Column(Float)
    ending_mud_volume = Column(Float)
    
    #gas
    max_gas = Column(Float)
    conn_gas = Column(Float)
    trip_gas = Column(Float)
    back_gas = Column(Float)

    #hydraulic analysis
    annular_velocity = Column(Float)
    pb = Column(Float)
    sys_hhp = Column(Float)
    hhpb = Column(Float)
    hsi = Column(Float)
    percent_psib = Column(Float)
    jet_velocity = Column(Float)
    impact_force = Column(Float)
    if_area = Column(Float)
    
    #hse
    stop_cards = Column(Integer)
    lta = Column(Enum(YesNo))
    spill = Column(Enum(YesNo))
    h2s_test = Column(Enum(YesNo))
    hse_mtg = Column(Enum(YesNo))
    kicktrip = Column(Enum(YesNo))
    kickdrill = Column(Enum(YesNo))
    fire = Column(Enum(YesNo))
    
    #lampiran
    time_breakdowns = relationship("TimeBreakdown", back_populates="daily_operations_report", lazy="joined")
    bit_records = relationship('BitRecord', back_populates='daily_operations_report')
    bottom_hole_assemblies = relationship('BottomHoleAssembly', back_populates='daily_operations_report')
    drilling_fluids = relationship('DrillingFluid', back_populates='daily_operations_report')
    mud_additives = relationship('MudAdditive', back_populates='daily_operations_report')
    bulk_materials = relationship('BulkMaterial', back_populates='daily_operations_report')
    Incidents = relationship("Incident", back_populates="daily_operations_report")
    personnel = relationship("Personnel", back_populates="daily_operations_report")
    directional_surveys = relationship('DirectionalSurvey', back_populates='daily_operations_report')
    pumps = relationship('Pumps', back_populates='daily_operations_report')
    weather = relationship('Weather', back_populates='daily_operations_report', uselist=False)

class JobCategory(PyEnum):
    DRILLING = 'DRILLING'
    COMPLETION = 'COMPLETION'
    WORKOVER = 'WORKOVER'

class NPT(PyEnum):
    NP = 'NP'
    P = 'P'

class DrillingOperation(PyEnum):
    RIG_UP_TEAR_DOWN = "(1) Rig Up and Tear Down"
    DRILL_ACTUAL = "(2) Drill Actual"
    REAMING = "(3) Reaming"
    CORING = "(4) Coring"
    CONDITION_MUD_CIRCULATE = "(5) Condition Mud & Circulate"
    TRIPS = "(6) Trips"
    LUBRICATE_RIG = "(7) Lubricate Rig"
    REPAIR_RIG = "(8) Repair Rig"
    CUT_OFF_DRILLING_LINE = "(9) Cut Off Drilling Line"
    DEVIATION_SURVEY = "(10) Deviation Survey"
    WIRE_LINE_LOGS = "(11) Wire Line Logs"
    RUN_CASING_CEMENT = "(12) Run Casing & Cement"
    WAIT_ON_CEMENT = "(13) Wait On Cement"
    NIPPLE_UP_BOP = "(14) Nipple Up B.O.P."
    TEST_BOP = "(15) Test B.O.P."
    DRILL_STEM_TEST = "(16) Drill Stem Test"
    PLUG_BACK = "(17) Plug Back"
    SQUEEZE_CEMENT = "(18) Squeeze Cement"
    FISHING = "(19) Fishing"
    DIR_WORK = "(20) Dir. Work"
    RUN_RETRIEVE_RISER_EQUIP = "(21) Run/Retrieve Riser Equip."
    SURFACE_TESTING = "(22) Surface Testing"
    OTHER = "(23) Other"

class CompletionOperation(PyEnum):
    PERFORATING = "(A) Perforating"
    TUBING_TRIPS = "(B) Tubing Trips"
    TREATING = "(C) Treating"
    SWABBING = "(D) Swabbing"
    TESTING = "(E) Testing"

class WorkoverOperation(PyEnum):
    SAND_CONTROL = "(c) Sand Control"
    WATER_SHUT_OFF = "(d) Water Shut Off"
    WELLBORE_CLEANOUT = "(e) Wellbore Cleanout"
    STANDBY = "(n) Standby"
    MOBILIZATION = "(o) Mobilization"
    OTHER = "(p) Other"

@extend_enum([DrillingOperation,CompletionOperation, WorkoverOperation])
class OperationCode(PyEnum):
   pass

class TimeBreakdown(Base):
    
    __tablename__ = 'job_time_breakdown'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship("DailyOperationsReport", back_populates="time_breakdowns")
    
    #time
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    
    #measured depth
    start_measured_depth = Column(Float)
    end_measured_depth = Column(Float)
    
    #task
    category = Column(Enum(JobCategory))
    p = Column(Enum(YesNo))
    npt = Column(Enum(NPT))
    code = Column(Enum(OperationCode))
    
    operation = Column(Text)
    code = Column(SQLAlchemyEnum(OperationCode, name='operationcode', create_constraint=False))

    @property
    def start_time_without_microseconds(self):
        return self.start_time.replace(microsecond=0) if self.start_time else None

    @property
    def end_time_without_microseconds(self):
        return self.end_time.replace(microsecond=0) if self.end_time else None

class BitRecord(Base):
    
    __tablename__ = 'job_bit_records'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bit_records')

    bit_number = Column(String(10))
    bit_size = Column(Float)
    bit_run = Column(Integer)
    manufacturer = Column(String(50))
    iadc_code = Column(String(50))
    jets = Column(String(50))
    serial = Column(String(50))
    depth_out = Column(Float)
    depth_in = Column(Float)
    meterage = Column(Float)
    bit_hours = Column(Float)
    nozzels = Column(Float)
    dull_grade = Column(String(50))

class BottomHoleAssembly(Base):
    __tablename__ = 'job_bottom_hole_assemblies'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bottom_hole_assemblies')
    
    bha_number = Column(String(50))
    bha_run = Column(Integer)
    
    components = relationship('BHAComponent', back_populates='bottom_hole_assembly')

class BHAComponentType(PyEnum):
    BUMPER_SUB = "Bumper Sub"
    CROSSOVER = "Crossover"
    DRILL_COLLAR = "Drill Collar"
    DRILL_PIPE = "Drill Pipe"
    FLEX_JOINT_COLLAR = "Flex Joint Collar"
    FLOAT_SUB = "Float Sub"
    HEAVY_WEIGHT_DRILL_PIPE = "Heavy Weight Drill Pipe (HWDP)"
    HOLE_OPENER = "Hole Opener"
    JAR = "Jar"
    JARS_BOOSTER = "Jars - Booster"
    JARS_HYDRAULIC = "Jars - Hydraulic"
    JARS_HYDRO_MECHANICAL = "Jars - Hydro Mechanical"
    JARS_MECHANICAL = "Jars - Mechanical"
    JUNK_SUB = "Junk Sub"
    KELLY_DOWN = "Kelly Down"
    MOTOR = "Motor"
    MWD_LWD = "MWD/LWD"
    NON_MAGNETIC_ANTENNA_SUB = "Non-Magnetic antenna sub"
    NON_MAGNETIC_COLLAR = "Non-Magnetic Collar"
    NON_MAGNETIC_INDEX_SUB = "Non-Magnetic Index Sub"
    NON_MAGNETIC_INTEGRAL_BLADE_STABILIZER = "Non-Magnetic Integral Blade Stabilizer"
    NON_MAGNETIC_PONY_COLLAR = "Non-Magnetic Pony Collar"
    NON_MAGNETIC_REPEATER_SUB = "Non-Magnetic Repeater sub"
    PORTED_FV = "Ported FV"
    REAMER = "Reamer"
    ROLLER_REAMER = "RollerReamer"
    ROTARY_STEERABLE = "Rotary Steerable"
    SAFETY_JOINT = "Safety Joint"
    SAVER_SUB = "Saver Sub"
    SENSOR = "Sensor"
    SHOCK_SUB = "Shock Sub"
    SHORT_COLLAR = "Short Collar"
    SINGLES_DRILL_PIPE = "Singles Drill Pipe"
    SPERRY_DRILL = "Sperry Drill"
    SPIRAL_COLLAR = "Spiral Collar"
    STABILIZER = "Stabilizer"
    STABILIZER_VARIABLE_GAUGE = "Stabilizer - Variable Gauge"
    STABILIZER_WELDED_BLADE = "Stabilizer - Welded Blade"
    STANDS_DRILL_PIPE = "Stands Drill Pipe"
    SUB_TOTCO = "Sub totco"

class BHAComponent(Base):
    
    __tablename__ = 'job_bottom_hole_assemblies_components'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    bottom_hole_assembly_id = Column(String(36), ForeignKey('job_bottom_hole_assemblies.id'))
    bottom_hole_assembly = relationship('BottomHoleAssembly', back_populates='components')
    
    component = Column(Enum(BHAComponentType))
    
    outer_diameter = Column(Float)
    length = Column(Float)

class MudType(PyEnum):
    LIQUID = 'LIQUID'
    DRY = 'DRY'

class DrillingFluid(Base):
    
    __tablename__ = 'job_drilling_fluids'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
     
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='drilling_fluids')
    
    mud_type = Column(Enum(MudType))
    time = Column(DateTime)
    mw_in = Column(Float)
    mw_out = Column(Float)
    temp_in = Column(Float)
    temp_out = Column(Float)
    pres_grad = Column(Float)
    visc = Column(Float)
    pv = Column(Float)
    yp = Column(Float)
    gels_10_sec = Column(Float)
    gels_10_min = Column(Float)
    fluid_loss = Column(Float)
    ph = Column(Float)
    solids = Column(Float)
    sand = Column(Float)
    water = Column(Float)
    oil = Column(Float)
    hgs = Column(Float)
    lgs = Column(Float)
    ltlp = Column(Float)
    hthp = Column(Float)
    cake = Column(Float)
    e_stb = Column(Float)
    pf = Column(Float)
    mf = Column(Float)
    pm = Column(Float)
    ecd = Column(Float)

class MudAdditive(Base):
    
    __tablename__ = 'job_mud_additives'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='mud_additives')
    
    mud_additive_type = Column(String(50))
    amount = Column(Float)
    
class BulkMaterial(Base):
    
    __tablename__ = 'job_bulk_materials'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bulk_materials')
    
    material_type = Column(String(50))
    material_name = Column(String(50))	
    material_uom = Column(String(50))
    received = Column(Float)
    consumed = Column(Float)
    returned = Column(Float)
    adjust = Column(Float)
    ending = Column(Float)

class Incident(Base):
    
    __tablename__ = 'job_hse_incidents'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='Incidents')
    
    incidents_time = Column(DateTime)
    incident = Column(String(50))
    incident_type = Column(String(50))
    comments = Column(Text)

class DirectionalSurvey(Base):
    
    __tablename__ = 'job_directional_surveys'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='directional_surveys')
    
    measured_depth = Column(Float)
    inclination = Column(Float)
    azimuth = Column(Float)

class Personnel(Base):
    
    __tablename__ = 'job_personnel'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='personnel')
    
    company = Column(String(50))
    people = Column(Integer)

class Pumps(Base):
    
    __tablename__ = 'job_pumps'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='pumps')
    
    slow_speed = Column(Enum(YesNo))
    circulate = Column(Float)
    strokes = Column(Float)
    pressure = Column(Float)
    liner_size = Column(Float)
    efficiency = Column(Float)

class Weather(Base):
    
    __tablename__ = 'job_weather'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='weather')
    
    temperature_high = Column(Float)
    temperature_low = Column(Float)
    chill_factor = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    barometric_pressure = Column(Float)
    wave_height = Column(Float)
    wave_current_speed = Column(Float)
    road_condition = Column(String(50))
    visibility = Column(String(50))