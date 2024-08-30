from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from backend.routers.job.models import *
from backend.routers.well.schemas import *

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

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

    phase: str
    depth_datum: DepthDatum
    
    depth_in: float
    depth_out: float
    depth_uom: DepthUOM
    
    operation_days: float
    
    class Meta:
        orm_model = JobOperationDay

class JobInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)

    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal
    
    job_operation_days: List[JobOperationDayBase]
    work_breakdown_structure: List[WorkBreakdownStructureBase]
    job_hazards: List[JobHazardBase]
    job_documents: List[JobDocumentBase]

class CreateExploration(JobInstanceBase):
    
    well: CreateWell
    
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
        orm_model = Exploration

class CreateDevelopment(JobInstanceBase):
    
    well: CreateWell
    
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
        orm_model = Development
        
class CreateWorkover(JobInstanceBase):
    
    well: CreateWell
    job_category: WOWSJobType
    
    onstream_oil: Decimal
    onstream_gas:  Decimal
    water_cut:  Decimal

    class Meta:
        orm_model = Workover

class CreateWellService(JobInstanceBase):
    
    well: CreateWell
    job_category: WOWSJobType
    
    onstream_oil: Decimal
    onstream_gas:  Decimal
    water_cut:  Decimal

    class Meta:
        orm_model = WellService

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

class ExplorationPlan(PlanJobBase):
    
    job_plan: CreateExploration

class DevelopmentPlan(PlanJobBase):
    
    job_plan: CreateDevelopment

class WorkoverPlan(PlanJobBase):
    
    job_plan: CreateWorkover

class WellServicePlan(PlanJobBase):
    
    job_plan: CreateWellService
    