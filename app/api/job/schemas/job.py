from typing import List
from app.api.job.models import *
from app.api.well.schemas import *
# from app.core.schema_operations import AllRequired

from pydantic import BaseModel, Field, computed_field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from app.core.constants import UnitType

class WBCustomSEventSchema(BaseModel):
    event: str
    start_date: date
    end_date: date
    remarks: Optional[str]
    
    class Meta:
        orm_model = WBSCustomEvent

    class Config:
        from_attributes = True

class WBSWRMEventSchema(BaseModel):
    start_date: date
    end_date: date
    remarks: Optional[str]
    
    class Meta:
        orm_model = WBSWRMEvent
    
    class Config:
        from_attributes = True
        
    
class WBSExplorationSchema(BaseModel):
    
    wrm_pembebasan_lahan: WBSWRMEventSchema
    wrm_ippkh: WBSWRMEventSchema
    wrm_ukl_upl: WBSWRMEventSchema
    wrm_amdal: WBSWRMEventSchema
    wrm_pengadaan_rig: WBSWRMEventSchema
    wrm_pengadaan_drilling_services: WBSWRMEventSchema
    wrm_pengadaan_lli: WBSWRMEventSchema
    wrm_persiapan_lokasi: WBSWRMEventSchema
    wrm_internal_kkks: WBSWRMEventSchema
    wrm_evaluasi_subsurface: WBSWRMEventSchema
    
    events: List[WBCustomSEventSchema]
    
    class Meta:
        orm_model = WorkBreakdownStructureDrilling
    
    class Config:
        from_attributes = True

class WBSDevelopmentSchema(BaseModel):
    
    wrm_pembebasan_lahan: WBSWRMEventSchema
    wrm_ippkh: WBSWRMEventSchema
    wrm_ukl_upl: WBSWRMEventSchema
    wrm_amdal: WBSWRMEventSchema
    wrm_pengadaan_rig: WBSWRMEventSchema
    wrm_pengadaan_drilling_services: WBSWRMEventSchema
    wrm_pengadaan_lli: WBSWRMEventSchema
    wrm_persiapan_lokasi: WBSWRMEventSchema
    wrm_internal_kkks: WBSWRMEventSchema
    wrm_evaluasi_subsurface: WBSWRMEventSchema
    wrm_cutting_dumping: WBSWRMEventSchema
    
    events: List[WBCustomSEventSchema]
    
    class Meta:
        orm_model = WorkBreakdownStructureDrilling
    
    class Config:
        from_attributes = True

class WBSWOWSSchema(BaseModel):
    
    wrm_internal_kkks: WBSWRMEventSchema
    wrm_pengadaan_equipment: WBSWRMEventSchema
    wrm_pengadaan_services: WBSWRMEventSchema
    wrm_pengadaan_handak: WBSWRMEventSchema
    wrm_pengadaan_octg: WBSWRMEventSchema
    wrm_pengadaan_lli: WBSWRMEventSchema
    wrm_pengadaan_artificial_lift: WBSWRMEventSchema
    wrm_sumur_berproduksi: WBSWRMEventSchema
    wrm_fasilitas_produksi: WBSWRMEventSchema
    wrm_persiapan_lokasi: WBSWRMEventSchema 
    wrm_well_integrity: WBSWRMEventSchema
    
    events: List[WBCustomSEventSchema]
    
    class Meta:
        orm_model = WorkBreakdownStructureWOWS
    
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
    
    job_operation_days: Optional[List[JobOperationDayBase]] = None
    job_hazards: Optional[List[JobHazardBase]] = None
    job_documents: Optional[List[JobDocumentBase]] = None

    class Config:
        from_attributes = True

class JobActualInstanceBase(BaseModel):
    
    start_date: date
    end_date: date
    total_budget: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    
    job_operation_days: Optional[List[JobOperationDayBase]] = None
    job_hazards: Optional[List[JobHazardBase]] = None
    job_documents: Optional[List[JobDocumentBase]] = None

    class Config:
        from_attributes = True

class CreatePlanExploration(JobPlanInstanceBase):
    
    work_breakdown_structure: Optional[WBSExplorationSchema] = None
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreatePlanWell
    
    wrm_pembebasan_lahan: Optional[bool] = True
    wrm_ippkh: Optional[bool] = True
    wrm_ukl_upl: Optional[bool] = True
    wrm_amdal: Optional[bool] = True
    wrm_pengadaan_rig: Optional[bool] = True
    wrm_pengadaan_drilling_services: Optional[bool] = True
    wrm_pengadaan_lli: Optional[bool] = True
    wrm_persiapan_lokasi: Optional[bool] = True
    wrm_internal_kkks: Optional[bool] = True
    wrm_evaluasi_subsurface: Optional[bool] = True

    class Meta:
        orm_model = PlanExploration
    class Config:
        from_attributes = True

class CreateDummyPlanExploration(CreatePlanExploration):
    
    well: CreateDummyPlanWell
        
class CreatePlanDevelopment(JobPlanInstanceBase):
    
    work_breakdown_structure: Optional[WBSDevelopmentSchema] = None
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreatePlanWell
    
    wrm_pembebasan_lahan: Optional[bool] = True
    wrm_ippkh: Optional[bool] = True
    wrm_ukl_upl: Optional[bool] = True
    wrm_amdal: Optional[bool] = True
    wrm_cutting_dumping: Optional[bool] = True
    wrm_pengadaan_rig: Optional[bool] = True
    wrm_pengadaan_drilling_services: Optional[bool] = True
    wrm_pengadaan_lli: Optional[bool] = True
    wrm_persiapan_lokasi: Optional[bool] = True
    wrm_internal_kkks: Optional[bool] = True
    wrm_evaluasi_subsurface: Optional[bool] = True
    
    class Meta:
        orm_model = PlanDevelopment
    class Config:
        from_attributes = True

class CreateDummyPlanDevelopment(CreatePlanDevelopment):
    
    well: CreateDummyPlanWell
        
class CreatePlanWorkover(JobPlanInstanceBase):
    
    work_breakdown_structure: Optional[WBSWOWSSchema] = None
    
    equipment: str
    equipment_specifications: str
    
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
    
    well_schematic: Optional[WellSchematicBase] = None

    class Meta:
        orm_model = PlanWorkover
    class Config:
        from_attributes = True
        
class CreatePlanWellService(JobPlanInstanceBase):
    
    work_breakdown_structure: Optional[WBSWOWSSchema] = None
    
    equipment: str
    equipment_specifications: str
    
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
    
    well_schematic: Optional[WellSchematicBase] = None

    class Meta:
        orm_model = PlanWellService
    class Config:
        from_attributes = True
        
class CreateActualExploration(JobActualInstanceBase):
    
    work_breakdown_structure: Optional[WBSExplorationSchema] = None
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreateActualWell
    
    wrm_pembebasan_lahan: Optional[Percentage] = Percentage.P0
    wrm_ippkh: Optional[Percentage] = Percentage.P0
    wrm_ukl_upl: Optional[Percentage] = Percentage.P0
    wrm_amdal: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_rig: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_drilling_services: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_lli: Optional[Percentage] = Percentage.P0
    wrm_persiapan_lokasi: Optional[Percentage] = Percentage.P0
    wrm_internal_kkks: Optional[Percentage] = Percentage.P0
    wrm_evaluasi_subsurface: Optional[Percentage] = Percentage.P0
    
    class Meta:
        orm_model = ActualExploration
    class Config:
        from_attributes = True

class UpdateActualExploration(JobActualInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: UpdateActualWell
    
    wrm_pembebasan_lahan: Optional[Percentage] = Percentage.P0
    wrm_ippkh: Optional[Percentage] = Percentage.P0
    wrm_ukl_upl: Optional[Percentage] = Percentage.P0
    wrm_amdal: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_rig: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_drilling_services: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_lli: Optional[Percentage] = Percentage.P0
    wrm_persiapan_lokasi: Optional[Percentage] = Percentage.P0
    wrm_internal_kkks: Optional[Percentage] = Percentage.P0
    wrm_evaluasi_subsurface: Optional[Percentage] = Percentage.P0
    

    class Meta:
        orm_model = ActualDevelopment
    class Config:
        from_attributes = True
        
class CreateActualDevelopment(JobActualInstanceBase):
    
    work_breakdown_structure: Optional[WBSDevelopmentSchema] = None
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: CreateActualWell
    
    wrm_pembebasan_lahan: Optional[Percentage] = Percentage.P0
    wrm_ippkh: Optional[Percentage] = Percentage.P0
    wrm_ukl_upl: Optional[Percentage] = Percentage.P0
    wrm_amdal: Optional[Percentage] = Percentage.P0
    wrm_cutting_dumping: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_rig: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_drilling_services: Optional[Percentage] = Percentage.P0
    wrm_pengadaan_lli: Optional[Percentage] = Percentage.P0
    wrm_persiapan_lokasi: Optional[Percentage] = Percentage.P0
    wrm_internal_kkks: Optional[Percentage] = Percentage.P0
    wrm_evaluasi_subsurface: Optional[Percentage] = Percentage.P0
    
    class Meta:
        orm_model = ActualDevelopment
    class Config:
        from_attributes = True
        
class UpdateActualDevelopment(JobActualInstanceBase):
    
    rig_name: str
    rig_type: RigType
    rig_horse_power: Decimal

    well: UpdateActualWell

    class Meta:
        orm_model = ActualDevelopment
    class Config:
        from_attributes = True

class CreateActualWorkover(JobActualInstanceBase):
    
    work_breakdown_structure: Optional[WBSWOWSSchema] = None
    
    equipment: str
    equipment_specifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    well_schematic: Optional[WellSchematicBase] = None
    
    class Meta:
        orm_model = ActualWorkover
    class Config:
        from_attributes = True

class UpdateActualWorkover(JobActualInstanceBase):
    
    equipment: str
    equipment_specifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    well_schematic: Optional[WellSchematicBase] = None
    
    class Meta:
        orm_model = ActualWorkover
    class Config:
        from_attributes = True
               
class CreateActualWellService(JobActualInstanceBase):
    
    work_breakdown_structure: Optional[WBSWOWSSchema] = None
    
    equipment: str
    equipment_specifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    well_schematic: Optional[WellSchematicBase] = None
    
    class Meta:
        orm_model = ActualWellService
    class Config:
        from_attributes = True

class UpdateActualWellService(JobActualInstanceBase):
    
    equipment: str
    equipment_specifications: str
    
    well_id: str
    
    job_category: WOWSJobType
    job_description: str
    
    #target
    onstream_oil: Decimal
    onstream_gas: Decimal
    onstream_water_cut: Decimal
    
    well_schematic: Optional[WellSchematicBase] = None
    
    class Meta:
        orm_model = ActualWellService
    class Config:
        from_attributes = True
        
class JobBase(BaseModel):
    
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
        
class CreateExplorationJob(JobBase):
    
    job_plan: CreatePlanExploration

class CreateDummyExplorationJob(CreateExplorationJob):
    
    job_plan: CreateDummyPlanExploration
    
class CreateDevelopmentJob(JobBase):
    
    job_plan: CreatePlanDevelopment

class CreateDummyDevelopmentJob(CreateDevelopmentJob):
    
    job_plan: CreateDummyPlanDevelopment

class CreateWorkoverJob(JobBase):       
    
    job_plan: CreatePlanWorkover

class CreateWellServiceJob(JobBase):
    
    job_plan: CreatePlanWellService
    
class SuratTajakSchema(BaseModel):
    
    file_id: str
    nomor_surat: str

class ExplorationWRM(BaseModel):
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
        from_attributes = True

class DevelopmentWRM(BaseModel):
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
        from_attributes = True

class WorkoverWRM(BaseModel):
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
        from_attributes = True



class WellServiceWRM(BaseModel):
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
        from_attributes = True

class JobIssueCreate(BaseModel):
    # job_id: str
    date_time: datetime
    severity: Severity
    description: str
    # resolved: bool = False
    # resolved_date_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobIssueEdit(JobIssueCreate):
    pass
    
class JobIssueResponse(JobIssueCreate):
    id: str
    resolved: bool = False
    resolved_date_time: Optional[datetime] = None
    
# class JobIssueUpdate(BaseModel):
#     resolved: bool = True
#     resolved_date_time: Optional[datetime] = None

#     class Config:
#         from_attributes = True

class ColoredDate(BaseModel):
    date: date
    color: str
    
class PPPDocument(BaseModel):
    file_id: str
    
    @computed_field
    @property  
    def document_type(self) -> JobDocumentType:
        return JobDocumentType.PPP
    
    class Meta:
        orm_model = JobDocument
    class Config:
        from_attributes = True

class ProposePPP(BaseModel):

    surat_pengajuan_ppp: PPPDocument
    nomor_surat_pengajuan_ppp: str
    
    # Field for Dokumen Persetujuan AFE/WP&B
    dokumen_persetujuan_afe: PPPDocument
    
    # Field for Dokumen Project Summary
    dokumen_project_summary: PPPDocument
    
    # Field for Dokumen Pernyataan
    dokumen_pernyataan: PPPDocument

    # Field for Dokumen Laporan Pekerjaan
    dokumen_laporan_pekerjaan: PPPDocument

    # Field for Dokumen Formulir
    dokumen_formulir: PPPDocument

    # Field for Dokumen Korespondensi
    dokumen_korespondensi: PPPDocument
    
    # Field for Dokumen Sumur Tidak Berproduksi
    dokumen_sumur_tidak_berproduksi: PPPDocument

    # Field for Dokumen Daftar Material
    dokumen_daftar_material: PPPDocument
    
    dokumen_lainnya: Optional[List[JobDocumentBase]]

class ApprovePPP(BaseModel):
    
    surat_pengajuan_ppp_approval: Optional[bool]
    dokumen_persetujuan_afe_approval: Optional[bool]
    dokumen_project_summary_approval: Optional[bool]
    dokumen_pernyataan_approval: Optional[bool]
    dokumen_laporan_pekerjaan_approval: Optional[bool]
    dokumen_formulir_approval: Optional[bool]
    dokumen_korespondensi_approval: Optional[bool]
    dokumen_sumur_tidak_berproduksi_approval: Optional[bool]
    dokumen_daftar_material_approval: Optional[bool]

class ValidateActualExploration(CreateActualExploration):
    
    well: ValidateWell
    
class ValidateActualDevelopment(CreateActualDevelopment):
    
    well: ValidateWell
    
class ValidateActualWorkover(CreateActualWorkover):
    
    well: ValidateWell
    
class ValidateActualWellService(CreateActualWellService):
    
    well: ValidateWell
    