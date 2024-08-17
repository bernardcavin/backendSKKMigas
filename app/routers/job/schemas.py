from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from app.routers.job.models import *
from app.routers.well.schemas import *

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CreateWorkBreakdownStructure(BaseModel):
    
    event: str
    start_date: datetime
    end_data: datetime
    remarks: str

class CreateJobDocument(BaseModel):

    title: str
    creator_name: str
    create_date: datetime
    
    media_type: MediaType
    document_type: str
    
    item_category: str
    item_sub_category: str
    
    digital_format: str
    
    original_file_name: str
    
    digital_size: float
    digital_size_uom: SizeUOM
    
    remark: str

class CreateDrillingHazard(BaseModel):
    
    hazard_type: HazardType
    hazard_description: str
    severity: Severity
    mitigation: str
    
    remark: str

class CreateBudget(BaseModel):

    tangible_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    intangible_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    total_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)

class CreateJobActivity(BaseModel):

    time: datetime
    
    measured_depth: float
    measured_depth_uoum: DepthUOM
    measured_depth_datum: DepthDatum
    
    true_vertical_depth: float
    true_vertical_depth_uoum: DepthUOM
    
    true_vertical_depth_sub_sea: float
    true_vertical_depth_sub_sea_uoum: DepthUOM
    
    daily_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    
    summary: str
    current_operations: str
    next_operations: str

class JobBase(BaseModel):

    contract_type: Optional[ContractType]
    
    job_type: Optional[JobType]
    
    afe_number: Optional[str]
    wpb_year: Optional[int]
    plan_start: Optional[datetime]
    plan_end: Optional[datetime]
    plan_total_budget: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    rig_name: Optional[str]
    rig_type: Optional[RigType]
    rig_horse_power: Optional[float]

# CreateWorkBreakdownStructure with id
class GetWorkBreakdownStructure(CreateWorkBreakdownStructure):
    id: str

# CreateJobDocument with id
class GetJobDocument(CreateJobDocument):
    id: str

# CreateDrillingHazard with id
class GetDrillingHazard(CreateDrillingHazard):
    id: str

# CreateBudget with id
class GetBudget(CreateBudget):
    id: str

# CreateJobActivity with id
class GetJobActivity(CreateJobActivity):
    id: str

class GetJobBase(JobBase):
   
    job_activity: List[GetJobActivity]
    budget: List[GetBudget]
    work_breakdown_structure: List[GetWorkBreakdownStructure]
    drilling_hazard: List[GetDrillingHazard]
    job_documents: List[GetJobDocument]

class CreateJobBase(JobBase):

    job_activity: List[CreateJobActivity]
    budget: List[CreateBudget]
    work_breakdown_structure: List[CreateWorkBreakdownStructure]
    drilling_hazard: List[CreateDrillingHazard]
    job_documents: List[CreateJobDocument]

class DrillingBase:
    drilling_class: DrillingClass

class CreateDrillingJob(DrillingBase,CreateJobBase):
    
    planned_well: CreateWell

class GetDrillingJob(DrillingBase,CreateJobBase):
    id: str
    planned_well: GetWell
    final_well: GetWell

class WOWSBase:

    wows_class: WOWSClass
    job_category: WOWSJobType

    field_id: str
    
    #current
    current_oil: Decimal
    current_gas: Decimal
    current_condensate: Decimal
    
    current_oil_water_cut: Decimal
    current_gas_water_cut: Decimal
    current_condensate_water_cut: Decimal
    
    #target
    target_oil: Decimal
    target_gas: Decimal
    target_condensate: Decimal
    
    target_oil_water_cut: Decimal
    target_gas_water_cut: Decimal
    target_condensate_water_cut: Decimal
    
    # #final
    # final_oil: Decimal
    # final_gas: Decimal
    # final_condensate: Decimal
    
    # final_oil_water_cut: Decimal
    # final_gas_water_cut: Decimal
    # final_condensate_water_cut: Decimal

class CreateWOWSJob(WOWSBase,CreateJobBase):
    well: CreateWell

class GetWOWSJob(WOWSBase,CreateJobBase):
    id: str
    well: GetWell

class PengajuanBase(BaseModel):

    tanggal_diajukan: datetime
    tanggal_ditolak: datetime
    tanggal_disetujui: datetime
    
    status: StatusPengajuan

class CreatePengajuanDrilling(BaseModel):

    job: CreateDrillingJob
    
class GetPengajuanDrilling(PengajuanBase):

    id: str
    job: GetDrillingJob

class CreatePengajuanWOWS(BaseModel):

    job: CreateWOWSJob

class GetPengajuanWOWS(PengajuanBase):

    id: str
    job: GetWOWSJob