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
    
    job_id: str
    
    data_phase: DataPhase
    
    event: str
    start_date: datetime
    end_data: datetime
    remarks: str

class CreateJobDocument(BaseModel):
    
    job_id: str

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
    
    job_id: str
    
    data_phase: DataPhase
    
    hazard_type: HazardType
    hazard_description: str
    severity: Severity
    mitigation: str
    
    remark: str

class CreateBudget(BaseModel):
    
    job_id: str
    
    data_phase: DataPhase

    tangible_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    intangible_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    total_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)

class CreateJobActivity(BaseModel):

    job_id: str

    data_phase: DataPhase

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

class CreateDrilling(BaseModel):
    date_created: Optional[datetime]
    last_edited: Optional[datetime]

    kkks_id: Optional[str] = Field(None, min_length=36, max_length=36)
    
    field_id: Optional[str] = Field(None, min_length=36, max_length=36)
    
    contract_type: Optional[ContractType]
    
    job_type: Optional[JobType]
    
    afe_number: Optional[str]
    wpb_year: Optional[int]
    plan_start: Optional[datetime]
    plan_end: Optional[datetime]
    plan_total_budget: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    actual_total_budget: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    rig_name: Optional[str]
    rig_type: Optional[RigType]
    rig_horse_power: Optional[float]
    
    created_by_id: Optional[str] = Field(None, min_length=36, max_length=36)
    planned_well_id: CreateWell
    
    job_activity: List[CreateJobActivity]
    budget: List[CreateBudget]
    work_breakdown_structure: List[CreateWorkBreakdownStructure]
    drilling_hazard: List[CreateDrillingHazard]
    job_documents: List[CreateJobDocument]

    class Config:
        orm_mode = True

class GetWorkBreakdownStructure(CreateWorkBreakdownStructure):
    id: str

class GetJobDocument(CreateJobDocument):
    id: str

class GetDrillingHazard(CreateDrillingHazard):
    id: str

class GetBudget(CreateBudget):
    id: str

class GetJobActivity(CreateJobActivity):
    id: str

class GetDrilling(BaseModel):
    id: str
    date_created: Optional[datetime]
    last_edited: Optional[datetime]

    kkks_id: Optional[str] = Field(None, min_length=36, max_length=36)
    field_id: Optional[str] = Field(None, min_length=36, max_length=36)
    
    contract_type: Optional[ContractType]
    job_type: Optional[JobType]
    
    afe_number: Optional[str]
    wpb_year: Optional[int]
    plan_start: Optional[datetime]
    plan_end: Optional[datetime]
    plan_total_budget: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    actual_total_budget: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    rig_name: Optional[str]
    rig_type: Optional[RigType]
    rig_horse_power: Optional[float]
    
    created_by_id: Optional[str] = Field(None, min_length=36, max_length=36)
    planned_well_id: GetWell
    
    job_activity: List[GetJobActivity]
    budget: List[GetBudget]
    work_breakdown_structure: List[GetWorkBreakdownStructure]
    drilling_hazard: List[GetDrillingHazard]
    job_documents: List[GetJobDocument]

    class Config:
        orm_mode = True

class CreatePengajuan(BaseModel):
    