from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from backend.routers.job.models import *
from backend.routers.well.schemas import *

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class JobBase(BaseModel):

    # KKKS information
    kkks_id: Optional[str]
    area_id: Optional[str]
    field_id: Optional[str]
    
    # Contract information
    contract_type: Optional[ContractType]
    afe_number: Optional[str]
    wpb_year: Optional[int]
    
    start_date: Optional[date]
    end_date: Optional[date]
    total_budget: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    
    # Rig information
    rig_name: Optional[str]
    rig_type: Optional[RigType]
    rig_horse_power: Optional[float]

class WorkBreakdownStructureBase(BaseModel):
    
    event: str
    start_date: date
    end_date: date
    remarks: str
    
    class Meta:
        orm_model = WorkBreakdownStructure

class JobHazardBase(BaseModel):

    hazard_type: Optional[HazardType]
    hazard_description: Optional[str]
    severity: Optional[Severity]
    mitigation: Optional[str]
    remark: Optional[str]
    
    class Meta:
        orm_model = JobHazard

class JobDocumentBase(BaseModel):
    
    file_id: Optional[str]
    
    title: Optional[str]
    creator_name: Optional[str]
    create_date: Optional[datetime]
    
    media_type: Optional[MediaType]
    document_type: Optional[str]
    
    item_category: Optional[str]
    item_sub_category: Optional[str]
    
    digital_format: Optional[str]
    original_file_name: Optional[str]
    
    digital_size: Optional[float]
    digital_size_uom: Optional[SizeUOM]
    
    remark: Optional[str]
    
    class Meta:
        orm_model = JobDocument

class JobOperationDayBase(BaseModel):

    phase: Optional[str]
    depth_datum: Optional[DepthDatum]
    
    depth_in: Optional[float]
    depth_out: Optional[float]
    depth_uom: Optional[DepthUOM]
    
    operation_days: Optional[float]
    
    class Meta:
        orm_model = JobOperationDay

class CreateJob(JobBase):

    job_operation_days: List[JobOperationDayBase]
    work_breakdown_structure: List[WorkBreakdownStructureBase]
    job_hazards: List[JobHazardBase]
    job_documents: List[JobDocumentBase]

class CreateExploration(CreateJob):
    
    well: CreateWell

    class Meta:
        orm_model = Exploration

class CreateDevelopment(CreateJob):
    
    well: CreateWell
    
    class Meta:
        orm_model = Development
        
class CreateWorkover(CreateJob):
    
    well: CreateWell
    job_category: Optional[WOWSJobType]
    
    onstream_oil: Optional[float]
    onstream_gas:  Optional[float]
    water_cut:  Optional[float]

    class Meta:
        orm_model = Workover

class CreateWellService(CreateJob):
    
    well: CreateWell
    job_category: Optional[WOWSJobType]
    
    onstream_oil: Optional[float]
    onstream_gas:  Optional[float]
    water_cut:  Optional[float]

    class Meta:
        orm_model = WellService

class CreatePlanningBase(BaseModel):
    
    pass
    
class CreateExplorationPlanning(CreatePlanningBase):
    
    proposed_job: CreateExploration
    
    class Meta:
        orm_model = Planning

class CreateDevelopmentPlanning(CreatePlanningBase):
    
    proposed_job: CreateDevelopment
    
    class Meta:
        orm_model = Planning

class CreateWorkoverPlanning(CreatePlanningBase):
    
    proposed_job: CreateDevelopment
    
    class Meta:
        orm_model = Planning

class CreateWellServicePlanning(CreatePlanningBase):
    
    proposed_job: CreateWellService
    
    class Meta:
        orm_model = Planning


