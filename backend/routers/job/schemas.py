from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from backend.routers.job.models import *
from backend.routers.well.schemas import *

from pydantic import BaseModel, Field,field_validator,validator
from typing import Optional
from datetime import datetime, date,timedelta
from decimal import Decimal
from datetime import date, time
from typing import Annotated
import re
from backend.utils.constants import UnitType


class JobBase(BaseModel):
    id: str
    wpb_year: int
    # ... field lainnya ...

class JobDetail(JobBase):
    # ... tambahkan field detail lainnya jika diperlukan ...

    class Config:
        from_attributes = True
class WorkBreakdownStructureBase(BaseModel):
    
    event: str
    start_date: date
    end_date: date
    remarks: Optional[str]
    
    class Meta:
        orm_model = WorkBreakdownStructure

class JobHazardBase(BaseModel):

    hazard_type: HazardType
    hazard_description: Optional[str]
    severity: Severity
    mitigation: str
    remark: Optional[str]
    
    class Meta:
        orm_model = JobHazard

class JobDocumentBase(BaseModel):
    
    file_id: str
    document_type: JobDocumentType
    remark: Optional[str]
    
    class Meta:
        orm_model = JobDocument

class JobOperationDayBase(BaseModel):

    unit_type: UnitType
    phase: str
    depth_datum: DepthDatum
    
    depth_in: float
    depth_out: float
    
    operation_days: float
    
    class Meta:
        orm_model = JobOperationDay

class JobPlanInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    
    job_operation_days: List[JobOperationDayBase]
    work_breakdown_structure: List[WorkBreakdownStructureBase]
    job_hazards: List[JobHazardBase]
    job_documents: List[JobDocumentBase]

class JobActualInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    
    job_operation_days: List[JobOperationDayBase]
    work_breakdown_structure: List[WorkBreakdownStructureBase]
    job_hazards: List[JobHazardBase]   
    job_documents: List[JobDocumentBase]

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

class ActualJobBase(BaseModel):

    #kkks information
    area_id: str
    field_id: str
    
    #contract information
    contract_type: ContractType
    
    afe_number: str
    wpb_year: int

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
    id: str

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

class PersonnelCreate(PersonnelBase):
    pass

class PersonnelInDB(PersonnelBase):
    id: str

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


class IncidentCreate(IncidentBase):
    pass

class IncidentInDB(IncidentBase):
    id: str

    class Config:
        from_attributes = True

class BitRecordBase(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime
    bit_type: str
    bit_size: float
    bit_count: int
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




    @validator('start_time', 'end_time')
    def validate_time(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                pass
        elif isinstance(v, datetime):
            return v
        
class BitRecordCreate(BitRecordBase):
    pass

class BitRecordInDB(BitRecordBase):
    pass
    class Config:
        from_attributes = True

class DailyOperationsReportCreate(DailyOperationsReportBase):
    job_id: str 
    personnel: List[PersonnelCreate]
    Incidents: List[IncidentCreate]
    time_breakdowns: List[TimeBreakdownCreate]
    bit_records: List[BitRecordCreate]

    @validator('time_breakdowns')
    def validate_time_breakdowns(cls, v, values):
        report_date = values.get('report_date')
        if report_date is None:
            raise ValueError('report_date is required')
        
        for tb in v:
            if isinstance(tb.start_time, datetime):
                tb.start_time = tb.start_time.time()
            if isinstance(tb.end_time, datetime):
                tb.end_time = tb.end_time.time()
            
            start_datetime = datetime.combine(report_date, tb.start_time)
            end_datetime = datetime.combine(report_date, tb.end_time)
            
            # If end_time is earlier than start_time, assume it's the next day
            if end_datetime <= start_datetime:
                end_datetime += timedelta(days=1)
            
            tb.start_time = start_datetime.time().replace(microsecond=0)
            tb.end_time = end_datetime.time().replace(microsecond=0)
        
        return v

class DailyOperationsReportUpdate(DailyOperationsReportBase):
    
    time_breakdowns: List[TimeBreakdownCreate]

class DailyOperationsReportInDB(DailyOperationsReportBase):
    id: str
    job_id: str
    time_breakdowns: List[TimeBreakdownInDB]
    personnel: List[PersonnelInDB]
    Incidents: List[IncidentInDB]
    bit_records: List[BitRecordInDB]

    class Config:
        orm_mode = True

class ReportResponse(BaseModel):
    data: DailyOperationsReportInDB
    status: int