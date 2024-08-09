from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from app.routers.job.models import DepthPath, DepthReferencePoint, TipePekerjaan

class LogPekerjaanSchema(BaseModel):
    
    id: str
    waktu: datetime
    kedalaman: float
    depth_path: DepthPath
    reference_point: DepthReferencePoint
    daily_cost: condecimal(max_digits=10, decimal_places=2) # type: ignore
    
    summary: str
    current_operations: str
    next_operations: str
    
    pekerjaan_id: str
    
class PekerjaanSchema(BaseModel):

    id: str
    kkks: str
    lapangan: str
    wilayah_kerja: str
    tipe_kontrak: str
    tipe_pekerjaan: TipePekerjaan
    no_afe: str
    tahun_wpnb: int
    status: str
    
    #plan
    plan_mulai: datetime
    plan_selesai: datetime
    plan_budget: condecimal(max_digits=10, decimal_places=2) # type: ignore
    plan_schedule: List

class EksplorasiSchema(PekerjaanSchema):
    pass

class EksploitasiSchema(PekerjaanSchema):
    pass

class WorkoverSchema(PekerjaanSchema):
    pass

class WellServiceSchema(PekerjaanSchema):
    pass


Job = Union[EksplorasiSchema,EksploitasiSchema, WorkoverSchema, WellServiceSchema]
