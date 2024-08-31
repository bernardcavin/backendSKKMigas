from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, Enum, Text, Boolean, Float, Date, func
from backend.routers.well.models import DepthDatum
from sqlalchemy.orm import relationship, declared_attr
from backend.database import Base
from enum import Enum as PyEnum
import uuid
from backend.utils.enum_operations import extend_enum
from backend.utils.constants import uom

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
    EXPLORATION = 'Exploration'
    DEVELOPMENT = 'Development'
    WORKOVER = 'Workover'
    WELLSERVICE = 'Well Service'
    
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
    
    last_edited = Column(DateTime, onupdate=func.utcnow())
    
    @declared_attr
    def last_edited_by_id(cls):
        return Column(String(36), ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class Job(Base, CreateBase, ValidationBase):
    
    __tablename__ = 'jobs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_type = Column(Enum(JobType))
    job_instance_type = Column(Enum(JobInstanceType))
    
    #kkks information
    kkks_id = Column(String(36), ForeignKey('kkks.id'))
    kkks = relationship('KKKS', back_populates='jobs')
    
    area_id = Column(String(36), ForeignKey('area.id'))
    area = relationship('Area', back_populates='jobs')
    
    field_id = Column(String(36), ForeignKey('fields.id'))
    field = relationship('Lapangan', back_populates='jobs')
    
    #contract information
    contract_type = Column(Enum(ContractType))
    
    afe_number = Column(String)
    wpb_year = Column(Integer)
    
    #Planning
    job_plan_id = Column(String(36), ForeignKey('job_instances.id'))
    job_plan = relationship('JobInstance', foreign_keys=[job_plan_id])
    
    date_proposed = Column(Date)
    date_returned = Column(Date)
    date_approved = Column(Date)
    
    planning_status = Column(Enum(PlanningStatus))
    
    #Operation
    actual_job_id = Column(String(36), ForeignKey('job_instances.id'))
    actual_job = relationship('JobInstance', foreign_keys=[actual_job_id])
    
    daily_operations_report = relationship('DailyOperationsReport', back_populates='job')
    
    date_started = Column(Date)
    date_finished = Column(Date)
    
    job_issues = relationship('JobIssue', back_populates='job')
    
    operation_status = Column(Enum(OperationStatus))
    
    #PPP
    date_ppp_proposed = Column(Date)
    date_ppp_approved = Column(Date)
    
    ppp_status = Column(Enum(PPPStatus))
    
    #CloseOut
    date_proposed = Column(Date)
    date_approved = Column(Date)
    
    closeout_status = Column(Enum(CloseOutStatus))
    
class JobInstance(Base):
    
    __tablename__ = 'job_instances'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_phase_type = Column(String)
    
    start_date = Column(Date)
    end_date = Column(Date)
    total_budget = Column(Numeric(precision=10, scale=2))

    job_operation_days = relationship('JobOperationDay', back_populates='job_instance')
    work_breakdown_structure = relationship('WorkBreakdownStructure', back_populates='job_instance')
    job_hazards = relationship('JobHazard', back_populates='job_instance')
    job_documents = relationship('JobDocument', back_populates='job_instance')
    
    __mapper_args__ = {
        "polymorphic_on": "job_phase_type",
    }

class PlanJob(JobInstance):
    
    __tablename__ = 'job_plans'

    id = Column(String(36), ForeignKey('job_instances.id'), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "plan",
    }

class ActualJob(JobInstance):
    
    __tablename__ = 'job_actuals'

    id = Column(String(36), ForeignKey('job_instances.id'), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "actual",
    }

class PlanExploration(PlanJob):
    
    __tablename__ = 'job_plan_exploration'
    
    id = Column(String(36), ForeignKey('job_plans.id'), primary_key=True)
    
    # rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    well_plan_id = Column(String(36), ForeignKey('well_plans.id'))
    well_plan = relationship('PlanWell', foreign_keys=[well_plan_id])
    
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

class PlanDevelopment(PlanJob):
    
    __tablename__ = 'job_plan_development'
    
    id = Column(String(36), ForeignKey('job_plans.id'), primary_key=True)

    # rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)
    
    well_plan_id = Column(String(36), ForeignKey('well_plans.id'))
    well_plan = relationship('PlanWell', foreign_keys=[well_plan_id])
    
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

class PlanWorkover(PlanJob):
    
    __tablename__ = 'job_plan_workover'
    
    id = Column(String(36), ForeignKey('job_plans.id'), primary_key=True)
    
    equipment = Column(String)
    equipment_sepesifications = Column(Text)
    
    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
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
    
    __mapper_args__ = {
        "polymorphic_identity": 'plan_workover',
    }

class PlanWellService(PlanJob):
    
    __tablename__ = 'job_plan_well_service'
    
    id = Column(String(36), ForeignKey('job_plans.id'), primary_key=True)
    
    equipment = Column(String)
    equipment_sepesifications = Column(Text)
    
    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
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
    
    __mapper_args__ = {
        "polymorphic_identity": 'plan_wellservice',
    }

class ActualExploration(ActualJob):
    
    __tablename__ = 'job_actual_exploration'
    
    id = Column(String(36), ForeignKey('job_actuals.id'), primary_key=True)
    
    # rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)

    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
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

class ActualDevelopment(ActualJob):
    
    __tablename__ = 'job_actual_development'
    
    id = Column(String(36), ForeignKey('job_actuals.id'), primary_key=True)

    # rig information
    rig_name = Column(String)
    rig_type = Column(Enum(RigType))
    rig_horse_power = Column(Float)
    
    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
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

class ActualWorkover(ActualJob):
    
    __tablename__ = 'job_actual_workover'
    
    id = Column(String(36), ForeignKey('job_actuals.id'), primary_key=True)
    
    equipment = Column(String)
    equipment_sepesifications = Column(Text)
    
    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    #target
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    __mapper_args__ = {
        "polymorphic_identity": 'actual_workover',
    }

class ActualWellService(ActualJob):
    
    __tablename__ = 'job_actual_well_service'
    
    id = Column(String(36), ForeignKey('job_actuals.id'), primary_key=True)
    
    equipment = Column(String)
    equipment_sepesifications = Column(Text)
    
    well_id = Column(String(36), ForeignKey('well_actuals.id'))
    well = relationship('ActualWell', foreign_keys=[well_id])
    
    job_category = Column(Enum(WOWSJobType))
    job_description = Column(Text)
    
    onstream_oil = Column(Float)
    onstream_gas = Column(Float)
    onstream_water_cut = Column(Float)
    
    __mapper_args__ = {
        "polymorphic_identity": 'actual_wellservice',
    }

class WorkBreakdownStructure(Base):
    
    __tablename__ = 'job_wbs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_instance_id = Column(String(36), ForeignKey('job_instances.id'))
    job_instance = relationship('JobInstance', back_populates='work_breakdown_structure')
    
    event = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    remarks = Column(Text)

class JobHazard(Base):
    
    __tablename__ = 'job_hazards'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_instance_id = Column(String(36), ForeignKey('job_instances.id'))
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

class JobDocument(Base):
    
    __tablename__ = 'job_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    job_instance_id = Column(String(36), ForeignKey('job_instances.id'))
    job_instance = relationship('JobInstance', back_populates='job_documents')

    file_id = Column(String(36), ForeignKey('files.id'))
    file = relationship('FileDB', foreign_keys=[file_id])
    
    document_type = Column(Enum(JobDocumentType))
    
    remark = Column(Text)
    
class JobOperationDay(Base):
    __tablename__ = 'job_operation_days'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    phase = Column(String)
    
    depth_datum = Column(Enum(DepthDatum))
    
    depth_in = Column(Float)
    depth_out = Column(Float)
    depth_uom = Column(String)  # Changed to String
    
    operation_days = Column(Float)
    
    job_instance_id = Column(String(36), ForeignKey('job_instances.id'))
    job_instance = relationship('JobInstance', back_populates='job_operation_days')

    def __init__(self, unit_type, *args, **kwargs):

        uom_map = uom.get(unit_type, {})
        self.depth_uom = uom_map.get('Depth', 'm')  # Default to meters if not found

        super().__init__(*args, **kwargs)
        
        
class JobIssue(Base):
    
    __tablename__ = 'job_issues'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    job_id = Column(String(36), ForeignKey('jobs.id'))
    job = relationship('Job', back_populates='job_issues')
    
    date_time = Column(DateTime)
    severity = Column(Enum(Severity))
    description = Column(Text)
    
    resolved = Column(Boolean)
    resolved_date_time = Column(DateTime)

class YesNo(PyEnum):
    Y = 'Y'
    N = 'N'

class DailyOperationsReport(Base):
    
    __tablename__ = 'job_daily_operations_reports'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
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
    time_breakdown = relationship('TimeBreakdown', back_populates='daily_operations_report')
    bit_records = relationship('BitRecord', back_populates='daily_operations_report')
    bottom_hole_assemblies = relationship('BottomHoleAssembly', back_populates='daily_operations_report')
    drilling_fluids = relationship('DrillingFluid', back_populates='daily_operations_report')
    mud_additives = relationship('MudAdditive', back_populates='daily_operations_report')
    bulk_materials = relationship('BulkMaterial', back_populates='daily_operations_report')
    hse_incidents = relationship('Incident', back_populates='daily_operations_report')
    directional_surveys = relationship('DirectionalSurvey', back_populates='daily_operations_report')
    personnel = relationship('Personnel', back_populates='daily_operations_report')
    pumps = relationship('Pumps', back_populates='daily_operations_report')
    weather = relationship('Weather', back_populates='daily_operations_report')

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
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='time_breakdown')
    
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

class BitRecord(Base):
    
    __tablename__ = 'job_bit_records'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bit_records')

    bit_number = Column(String)
    bit_size = Column(Float)
    bit_run = Column(Integer)
    manufacturer = Column(String)
    iadc_code = Column(String)
    jets = Column(String)
    serial = Column(String)
    depth_out = Column(Float)
    depth_in = Column(Float)
    meterage = Column(Float)
    bit_hours = Column(Float)
    nozzels = Column(Float)
    dull_grade = Column(String)

class BottomHoleAssembly(Base):
    __tablename__ = 'job_bottom_hole_assemblies'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bottom_hole_assemblies')
    
    bha_number = Column(String)
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
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
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
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
     
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
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='mud_additives')
    
    mud_additive_type = Column(String)
    amount = Column(Float)
    
class BulkMaterial(Base):
    
    __tablename__ = 'job_bulk_materials'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='bulk_materials')
    
    material_type = Column(String)
    material_name = Column(String)	
    material_uom = Column(String)
    received = Column(Float)
    consumed = Column(Float)
    returned = Column(Float)
    adjust = Column(Float)
    ending = Column(Float)

class Incident(Base):
    
    __tablename__ = 'job_hse_incidents'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='hse_incidents')
    
    incidents_time = Column(DateTime)
    incident = Column(String)
    incident_type = Column(String)
    comments = Column(Text)

class DirectionalSurvey(Base):
    
    __tablename__ = 'job_directional_surveys'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='directional_surveys')
    
    measured_depth = Column(Float)
    inclination = Column(Float)
    azimuth = Column(Float)

class Personnel(Base):
    
    __tablename__ = 'job_personnel'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    daily_operations_report_id = Column(String(36), ForeignKey('job_daily_operations_reports.id'))
    daily_operations_report = relationship('DailyOperationsReport', back_populates='personnel')
    
    company = Column(String)
    people = Column(Integer)

class Pumps(Base):
    
    __tablename__ = 'job_pumps'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
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
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
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
    road_condition = Column(String)
    visibility = Column(String)