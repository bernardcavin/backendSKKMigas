from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json, computed_field
from datetime import datetime

from app.api.job.models import *
from app.api.well.schemas import *

from pydantic import BaseModel, Field,ConfigDict,Field,field_validator,validator, ValidationInfo
from typing import Optional,Annotated
from datetime import datetime, date,timedelta,time
from decimal import Decimal
import re

from app.core.constants import UnitType

class WorkBreakdownStructureBase(BaseModel):
    
    event: str
    start_date: date
    end_date: date
    remarks: Optional[str]
    
    class Meta:
        orm_model = WorkBreakdownStructure
    
    class Config:
        from_attributes = True

class JobHazardBase(BaseModel):

    hazard_type: HazardType
    hazard_description: Optional[str]
    severity: Severity
    mitigation: str
    remark: Optional[str]
    
    class Meta:
        orm_model = JobHazard

    class Config:
        from_attributes = True
        
class JobDocumentBase(BaseModel):
    
    file_id: str
    document_type: JobDocumentType
    remark: Optional[str]
    
    class Meta:
        orm_model = JobDocument
    class Config:
        from_attributes = True
        
class JobOperationDayBase(BaseModel):

    unit_type: UnitType
    phase: str
    depth_datum: DepthDatum
    
    depth_in: float
    depth_out: float
    
    operation_days: float
    
    class Meta:
        orm_model = JobOperationDay
    class Config:
        from_attributes = True
        
class JobPlanInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    
    job_operation_days: List[Optional[JobOperationDayBase]] = []
    work_breakdown_structure: List[Optional[WorkBreakdownStructureBase]] = []
    job_hazards: List[Optional[JobHazardBase]] = []
    job_documents: List[Optional[JobDocumentBase]] = []

    class Config:
        from_attributes = True

class JobActualInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    
    job_operation_days: List[Optional[JobOperationDayBase]] = []
    work_breakdown_structure: List[Optional[WorkBreakdownStructureBase]] = []
    job_hazards: List[Optional[JobHazardBase]] = []
    job_documents: List[Optional[JobDocumentBase]] = []

    class Config:
        from_attributes = True

class CreatePlanExploration(JobPlanInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreatePlanWell
    
    wrm_pembebasan_lahan: bool
    wrm_ippkh: bool
    wrm_ukl_upl: bool
    wrm_amdal: bool
    wrm_pengadaan_rig: bool
    wrm_pengadaan_drilling_services: bool
    wrm_pengadaan_lli: bool
    wrm_persiapan_lokasi: bool
    wrm_internal_kkks: bool
    wrm_evaluasi_subsurface: bool

    class Meta:
        orm_model = PlanExploration
    class Config:
        from_attributes = True
        
class CreatePlanDevelopment(JobPlanInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreatePlanWell
    
    wrm_pembebasan_lahan: bool
    wrm_ippkh: bool
    wrm_ukl_upl: bool
    wrm_amdal: bool
    wrm_cutting_dumping: bool
    wrm_pengadaan_rig: bool
    wrm_pengadaan_drilling_services: bool
    wrm_pengadaan_lli: bool
    wrm_persiapan_lokasi: bool
    wrm_internal_kkks: bool
    wrm_evaluasi_subsurface: bool
    
    class Meta:
        orm_model = PlanDevelopment
    class Config:
        from_attributes = True
        
class CreatePlanWorkover(JobPlanInstanceBase):
    
    equipment: str
    equipment_sepesifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #current
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    #target
    target_oil: Decimal
    target_gas: Decimal
    target_water_cut: Decimal

    class Meta:
        orm_model = PlanWorkover
    class Config:
        from_attributes = True
        
class CreatePlanWellService(JobPlanInstanceBase):
    
    equipment: str
    equipment_sepesifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #current
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    #target
    target_oil: Decimal
    target_gas: Decimal
    target_water_cut: Decimal

    class Meta:
        orm_model = PlanWellService
    class Config:
        from_attributes = True
        
class CreateActualExploration(JobActualInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreateActualWell
    
    wrm_pembebasan_lahan: Percentage
    wrm_ippkh: Percentage
    wrm_ukl_upl: Percentage
    wrm_amdal: Percentage
    wrm_pengadaan_rig: Percentage
    wrm_pengadaan_drilling_services: Percentage
    wrm_pengadaan_lli: Percentage
    wrm_persiapan_lokasi: Percentage
    wrm_internal_kkks: Percentage
    wrm_evaluasi_subsurface: Percentage
    
    class Meta:
        orm_model = ActualExploration
    class Config:
        from_attributes = True
        
class CreateActualDevelopment(JobActualInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreateActualWell
    
    wrm_pembebasan_lahan: Percentage
    wrm_ippkh: Percentage
    wrm_ukl_upl: Percentage
    wrm_amdal: Percentage
    wrm_cutting_dumping: Percentage
    wrm_pengadaan_rig: Percentage
    wrm_pengadaan_drilling_services: Percentage
    wrm_pengadaan_lli: Percentage
    wrm_persiapan_lokasi: Percentage
    wrm_internal_kkks: Percentage
    wrm_evaluasi_subsurface: Percentage
    
    class Meta:
        orm_model = ActualDevelopment
    class Config:
        from_attributes = True
           
class CreateActualWorkover(JobActualInstanceBase):
    
    equipment: str
    equipment_sepesifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    class Meta:
        orm_model = ActualWorkover
    class Config:
        from_attributes = True
           
class CreateActualWellService(JobActualInstanceBase):
    
    equipment: str
    equipment_sepesifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    class Meta:
        orm_model = ActualWellService
    class Config:
        from_attributes = True
        
class PlanJobBase(BaseModel):
    
    #kkks information
    area_id: str
    field_id: str
   
    #contract information
    contract_type: ContractType
    
    afe_number: str
    wpb_year: int
    
    class Meta:
        orm_model = Job
    class Config:
        from_attributes = True
        
class ActualJobBase(BaseModel):
    
    #contract information
    contract_type: ContractType
    
    afe_number: str
    wpb_year: int
    
    class Config:
        from_attributes = True
        
class ExplorationJobPlan(PlanJobBase):
    
    job_plan: CreatePlanExploration

class DevelopmentJobPlan(PlanJobBase):
    
    job_plan: CreatePlanDevelopment

class WorkoverJobPlan(PlanJobBase):
    
    job_plan: CreatePlanWorkover

class WellServiceJobPlan(PlanJobBase):
    
    job_plan: CreatePlanWellService

class ExplorationActualJob(ActualJobBase):
    
    actual_job: CreateActualExploration

class DevelopmentActualJob(ActualJobBase):
    
    actual_job: CreateActualDevelopment

class WorkoverActualJob(ActualJobBase):
    
    actual_job: CreateActualWorkover

class WellServiceActualJob(ActualJobBase):
    
    actual_job: CreateActualWellService
    
def validate_time(v):
    if isinstance(v, time):
        return v
    if isinstance(v, datetime):
        return v.time()
    if isinstance(v, str):
        iso_pattern = r'^(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?(Z|[+-]\d{2}:?\d{2})?$'
        simple_pattern = r'^(\d{2}):(\d{2}):(\d{2})$'
        
        iso_match = re.match(iso_pattern, v)
        simple_match = re.match(simple_pattern, v)
        
        if iso_match:
            hour, minute, second = map(int, iso_match.group(1, 2, 3))
            microsecond = int(iso_match.group(4) or '0')
            return time(hour, minute, second, microsecond)
        elif simple_match:
            hour, minute, second = map(int, simple_match.groups())
            return time(hour, minute, second)
    


# Definisikan TimeField sebagai Annotated type
TimeField = Annotated[time, Field(json_schema_extra={"type": "string", "format": "time"})]

class TimeBreakdownBase(BaseModel):
    start_time: time
    end_time: time
    start_measured_depth: float
    end_measured_depth: float
    category: JobCategory
    p: YesNo
    npt: NPT
    code: str
    operation: str

    code: OperationCode

    class Meta:
        orm_model = TimeBreakdown
    
    @validator('start_time', 'end_time', pre=True)
    def parse_time(cls, v):
        if isinstance(v, str):
            # Remove the 'Z' if present
            v = v.rstrip('Z')
            
            # Use regex to parse time with optional milliseconds
            match = re.match(r'(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?', v)
            if match:
                hour, minute, second, microsecond = match.groups()
                microsecond = microsecond or '0'
                microsecond = microsecond.ljust(6, '0')[:6]  # Ensure 6 digits
                return time(int(hour), int(minute), int(second), int(microsecond))
            raise ValueError(f"Invalid time format: {v}")
        elif isinstance(v, time):
            return v
        elif isinstance(v, datetime):
            return v.time()
        raise ValueError(f"Invalid time type: {type(v)}")

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        start = values.get('start_time')
        if start is not None and v <= start:
            raise ValueError('end_time must be after start_time')
        return v

class TimeBreakdownCreate(TimeBreakdownBase):
    pass

class TimeBreakdownInDB(TimeBreakdownBase):
    class Config:
        from_attributes = True



class DailyOperationsReportBase(BaseModel):
    report_date: date
    avg_wob: float
    avg_rop: float
    avg_rpm: float
    torque: float
    stand_pipe_pressure: float
    flow_rate: float
    string_weight: float
    rotating_weight: float
    total_drilling_time: float
    circulating_pressure: float
    daily_cost: float
    daily_mud_cost: float
    day_supervisor: float
    night_supervisor: float
    engineer: float
    geologist: float
    day_summary: str
    day_forecast: str
    last_size: float
    set_md: float
    next_size: float
    next_set_md: float
    last_lot_emw: float
    tol: float
    start_mud_volume: float
    lost_surface_mud_volume: float
    lost_dh_mud_volume: float
    dumped_mud_volume: float
    built_mud_volume: float
    ending_mud_volume: float
    max_gas: float
    conn_gas: float
    trip_gas: float
    back_gas: float
    annular_velocity: float
    pb: float
    sys_hhp: float
    hhpb: float
    hsi: float
    percent_psib: float
    jet_velocity: float
    impact_force: float
    if_area: float
    stop_cards: int
    lta: YesNo
    spill: YesNo
    h2s_test: YesNo
    hse_mtg: YesNo
    kicktrip: YesNo
    kickdrill: YesNo
    fire: YesNo


class PersonnelBase(BaseModel):
    company: str
    people: int

    class Meta:
        orm_model = Personnel

class PersonnelCreate(PersonnelBase):
    pass

class PersonnelInDB(PersonnelBase):

    class Config:
        from_attributes = True


class IncidentBase(BaseModel):
    incidents_time: datetime
    incident: str
    incident_type: str
    comments: Optional[str] = None
    

    @validator('incidents_time', pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            # Remove milliseconds and 'Z'
            value = re.sub(r'\.\d+Z?$', '', value)
            try:
                dt = datetime.fromisoformat(value)
            except ValueError:
                try:
                    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    raise ValueError("Invalid datetime format")
            # Ensure microseconds are removed
            return dt.replace(microsecond=0)
        elif isinstance(value, datetime):
            # If it's already a datetime object, ensure microseconds are removed
            return value.replace(microsecond=0)
        return value

    class Meta:
        orm_model = Incident

class IncidentCreate(IncidentBase):
    pass

class IncidentInDB(IncidentBase):
    class Config:
        from_attributes = True

class BitRecordBase(BaseModel):
    bit_size: float
    bit_number: int
    bit_run: int
    manufacturer: str
    iadc_code: str
    jets: str
    serial: str
    depth_out: float
    depth_in: float
    meterage: float
    bit_hours: float
    nozzels: float
    dull_grade: str

    class Meta:
        orm_model = BitRecord
        
class BitRecordCreate(BitRecordBase):
    pass

class BitRecordInDB(BitRecordBase):
    pass
    class Config:
        from_attributes = True


class BHAComponentBase(BaseModel):
    component: BHAComponentType
    outer_diameter: float
    length: float

    class Meta:
        orm_model = BHAComponent

class BHAComponentCreate(BHAComponentBase):
    pass

class BHAComponentInDB(BHAComponentBase):
    pass
    model_config = ConfigDict(from_attributes=True)

class BottomHoleAssemblyBase(BaseModel):

    bha_number: int
    bha_run: int

    class Meta:
        orm_model = BottomHoleAssembly

class BottomHoleAssemblyCreate(BottomHoleAssemblyBase):
    components: List[BHAComponentCreate]

class BottomHoleAssemblyInDB(BottomHoleAssemblyBase):
    components: List[BHAComponentInDB]

    model_config = ConfigDict(from_attributes=True)

class DrillingFluidBase(BaseModel):
    mud_type: MudType
    time: datetime
    mw_in: float
    mw_out: float
    temp_in: float
    temp_out: float
    pres_grad: float
    visc: float
    pv: float
    yp: float
    gels_10_sec: float
    gels_10_min: float
    fluid_loss: float
    ph: float
    solids: float
    sand: float
    water: float
    oil: float
    hgs: float
    lgs: float
    ltlp: float
    hthp: float
    cake: float
    e_stb: float
    pf: float
    mf: float
    pm: float
    ecd: float

    class Meta:
        orm_model = DrillingFluid

class DrillingFluidCreate(DrillingFluidBase):
    pass

class DrillingFluidInDB(DrillingFluidBase):
    pass
    model_config = ConfigDict(from_attributes=True)

class MudAdditiveBase(BaseModel):
    mud_additive_type: str
    amount: float

    class Meta:
        orm_model = MudAdditive

class MudAdditiveCreate(MudAdditiveBase):
    pass

class MudAdditiveInDB(MudAdditiveBase):
    pass
    model_config = ConfigDict(from_attributes=True)

class BulkMaterialBase(BaseModel):
    material_type: str
    material_name: str
    material_uom: str
    received: float
    consumed: float
    returned: float
    adjust: float
    ending: float

    class Meta:
        orm_model = BulkMaterial

class BulkMaterialCreate(BulkMaterialBase):
    pass

class BulkMaterialInDB(BulkMaterialBase):

    model_config = ConfigDict(from_attributes=True)

class DirectionalSurveyBase(BaseModel):
    measured_depth: float
    inclination: float
    azimuth: float

    class Meta:
        orm_model = DirectionalSurvey

class DirectionalSurveyCreate(DirectionalSurveyBase):
    pass

class DirectionalSurveyInDB(DirectionalSurveyBase):

    model_config = ConfigDict(from_attributes=True)

class PumpsBase(BaseModel):
    slow_speed: YesNo
    circulate: float
    strokes: float
    pressure: float
    liner_size: float
    efficiency: float

    class Meta:
        orm_model = Pumps

class PumpsCreate(PumpsBase):
    pass

class PumpsInDB(PumpsBase):

    model_config = ConfigDict(from_attributes=True)

class WeatherBase(BaseModel):
    temperature_high: float
    temperature_low: float
    chill_factor: float
    wind_speed: float
    wind_direction: float
    barometric_pressure: float
    wave_height: float
    wave_current_speed: float
    road_condition: str
    visibility: str

    class Meta:
        orm_model = Weather

class WeatherCreate(WeatherBase):
    pass

class WeatherInDB(WeatherBase):

    model_config = ConfigDict(from_attributes=True)


class DailyOperationsReportCreate(DailyOperationsReportBase):
    job_id: str 
    personnel: List[PersonnelCreate]
    Incidents: List[IncidentCreate]
    time_breakdowns: List[TimeBreakdownCreate]
    bit_records: List[BitRecordCreate]
    bottom_hole_assemblies: List[BottomHoleAssemblyCreate]
    drilling_fluids: List[DrillingFluidCreate]
    mud_additives: List[MudAdditiveCreate]
    bulk_materials: List[BulkMaterialCreate]
    directional_surveys: List[DirectionalSurveyCreate]
    pumps: List[PumpsCreate]
    weather: WeatherCreate

    class Meta:
        orm_model = DailyOperationsReport

class DailyOperationsReportUpdate(DailyOperationsReportBase):
    
    time_breakdowns: List[TimeBreakdownCreate]

class DailyOperationsReportInDB(DailyOperationsReportBase):
    id: str
    job_id: str
    time_breakdowns: List[TimeBreakdownInDB]
    personnel: List[PersonnelInDB]
    Incidents: List[IncidentInDB]
    bit_records: List[BitRecordInDB]
    bottom_hole_assemblies: List[BottomHoleAssemblyInDB]
    drilling_fluids: List[DrillingFluidInDB]
    mud_additives: List[MudAdditiveInDB]
    bulk_materials: List[BulkMaterialInDB]
    directional_surveys: List[DirectionalSurveyInDB]
    pumps: List[PumpsInDB]
    weather: WeatherInDB


    model_config = ConfigDict(from_attributes=True)

class ReportResponse(BaseModel):
    data: DailyOperationsReportInDB
    status: int

class ActualExplorationUpdate(BaseModel):
    wrm_pembebasan_lahan: Optional[Percentage] = None
    wrm_ippkh: Optional[Percentage] = None
    wrm_ukl_upl: Optional[Percentage] = None
    wrm_amdal: Optional[Percentage] = None
    wrm_pengadaan_rig: Optional[Percentage] = None
    wrm_pengadaan_drilling_services: Optional[Percentage] = None
    wrm_pengadaan_lli: Optional[Percentage] = None
    wrm_persiapan_lokasi: Optional[Percentage] = None
    wrm_internal_kkks: Optional[Percentage] = None
    wrm_evaluasi_subsurface: Optional[Percentage] = None

    class Config:
        orm_mode = True

class JobIssueCreate(BaseModel):
    job_id: str
    date_time: datetime = Field(default_factory=datetime.utcnow)
    severity: Severity
    description: str
    resolved: bool = False
    resolved_date_time: Optional[datetime] = None

    class Config:
        orm_mode = True

class JobIssueResponse(JobIssueCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))