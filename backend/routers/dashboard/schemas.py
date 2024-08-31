from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
from datetime import date
from backend.routers.job.schemas import *
from backend.routers.well.schemas import *



router = APIRouter()

class WellData(BaseModel):
    well_name: Optional[str]

    class Config:
        from_attributes = True

class JobData(BaseModel):
    start_date: Optional[date]

    class Config:
        from_attributes = True

class CombinedData(BaseModel):
    wells: List[WellData]
    jobs: List[JobData]


class JobTypeData(BaseModel):
    count: int
    approved: int
    active: int
    percentage: float

class JobTypeData(BaseModel):
    approved_plans: int
    active_operations: int
    percentage: float

class KKKSJobData(BaseModel):
    id: str
    nama_kkks: str
    exploration: JobTypeData
    development: JobTypeData
    workover: JobTypeData
    wellservice: JobTypeData

class JobTypeSummary(BaseModel):
    job_type: str
    rencana: int
    realisasi: int
    selesai: int

class ExplorationRealizationItem(BaseModel):
    kkks_id: str
    kkks_name: str
    approved_plans: int
    completed_operations: int
    realization_percentage: float

class ExplorationRealizationResponse(BaseModel):
    data: List[ExplorationRealizationItem]


class ChartData(BaseModel):
    data: List[Dict]
    layout: Dict

class BudgetSummaryResponse(BaseModel):
    charts: Dict[str, ChartData]


class TimeSeriesData(BaseModel):
    time_period: str
    planned: int
    realized: int

class ChartDataModal(BaseModel):
    chart_json: str

class WellJobData(BaseModel):
    nama_sumur: str
    wilayah_kerja: str
    lapangan: Optional[str] 
    tanggal_mulai: str
    tanggal_selesai: str
    tanggal_realisasi: Optional[str] 
    status: str

class KKKSDetailResponse(BaseModel):
    kkks_name: str
    total_jobs: int
    approved_jobs: Optional[int]
    operating_jobs: Optional[int]
    finished_jobs: Optional[int]
    monthly_data: List[TimeSeriesData]
    weekly_data: List[TimeSeriesData]
    chart_data: ChartDataModal
    well_job_data: List[WellJobData]


class JobCountResponse(BaseModel):
    job_type: str
    status: str
    count: int

class JobTypeDataUP(BaseModel):
    total: int
    plan: int
    realization: int
    percentage: float
    change: int

class AggregateJobData(BaseModel):
    exploration: JobTypeDataUP
    development: JobTypeDataUP
    workover: JobTypeDataUP
    wellservice: JobTypeDataUP




