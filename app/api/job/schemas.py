from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from app.api.job.models import *
from app.api.well.schemas import *

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

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

    #kkks information
    area_id: str
    field_id: str
    
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
    
    