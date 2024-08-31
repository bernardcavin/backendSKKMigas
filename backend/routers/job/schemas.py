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

class JobPlanInstanceBase(BaseModel):
    
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

    well_plan: CreatePlanWell
    
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

    well_plan: CreatePlanWell
    
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

class ExplorationJobPlan(PlanJobBase):
    
    job_plan: CreatePlanExploration

class DevelopmentJobPlan(PlanJobBase):
    
    job_plan: CreatePlanDevelopment

class WorkoverJobPlan(PlanJobBase):
    
    job_plan: CreatePlanWorkover

class WellServiceJobPlan(PlanJobBase):
    
    job_plan: CreatePlanWellService
    