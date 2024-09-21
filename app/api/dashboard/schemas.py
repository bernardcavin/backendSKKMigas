from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel,RootModel
from datetime import date
from app.api.job.schemas import *
from app.api.well.schemas import *



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
    finished_jobs: int
    percentage: float


class JobTypeDataP(BaseModel):
    approved_plans: int
    active_operations: int
    finished_jobs: int
    percentage: float


class KKKSJobData(BaseModel):
    id: str
    name: str
    exploration: JobTypeDataP
    development: JobTypeDataP
    workover: JobTypeDataP
    wellservice: JobTypeDataP

class JobTypeSummary(BaseModel):
    job_type: str
    rencana: int
    realisasi: int
    selesai: int

class RealizationItem(BaseModel):
    kkks_id: str
    kkks_name: str
    job_type: str
    approved_plans: int
    completed_operations: int
    realization_percentage: float


class ExplorationRealizationResponse(BaseModel):
    data: List[RealizationItem]


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
    tanggal_mulai: Optional[str]
    tanggal_selesai: Optional[str]
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


class BudgetSummary(BaseModel):
    exploration: Dict[str, float]
    development: Dict[str, float]
    workover: Dict[str, float]
    wellservice: Dict[str, float]

class JobWellStatusSummary(BaseModel):
    post_operation_count: int
    well_status: Dict[str, int]

class DashboardData(BaseModel):
    budget_summary: BudgetSummary
    job_well_status: JobWellStatusSummary
    exploration_realization: List[RealizationItem]

class JobTypeDataKKKS(BaseModel):
    approved_plans: int
    active_operations: int
    percentage: float

class JobTypeTimeSeriesData(BaseModel):
    exploration: Optional[List[TimeSeriesData]] = None
    development: Optional[List[TimeSeriesData]] = None
    workover: Optional[List[TimeSeriesData]] = None
    well_service: Optional[List[TimeSeriesData]] = None


class ChartAxis(BaseModel):
    title: str
    tickmode: Optional[str] = None
    tickvals: Optional[List] = None
    ticktext: Optional[List] = None
    tickangle: Optional[int] = None
    range: Optional[List[float]] = None

class ChartLayout(BaseModel):
    title: str
    xaxis: ChartAxis
    yaxis: ChartAxis
    barmode: Optional[str] = None
    bargap: Optional[float] = None
    bargroupgap: Optional[float] = None

class ChartDataItem(BaseModel):
    type: str
    name: str
    x: List
    y: List
    marker: Optional[dict] = None


class ChartDataKKKS(BaseModel):
    data: List[ChartDataItem]
    layout: ChartLayout

class KKKSJobDataChart(BaseModel):
    id: str
    name: str
    job_data: JobTypeData
    monthly_data: Dict[str, List[TimeSeriesData]]
    weekly_data: Dict[str, List[TimeSeriesData]]
    well_job_data: Dict[str, List[WellJobData]]
    chart_data: Dict[str, Dict[str, ChartDataKKKS]]

class JobResponse(BaseModel):
    id: str
    well_name: str
    name: str
    name: str
    date_proposed: Optional[str]
    date_approved: Optional[str]
    date_started: Optional[str]
    planning_status: PlanningStatus

class JobTypeGroup(BaseModel):
    root: Dict[str, List[JobResponse]]

    class Config:
        from_attributes = True

class JobCounts(BaseModel):
    total_count: int
    post_operation_count: int

class JobTypeSummaryPie(BaseModel):
    well_status: Dict[str, int]
    chart: str

class JobAndWellStatusSummary(BaseModel):
    exploration: JobTypeSummaryPie
    development: JobTypeSummaryPie
    well_status: Dict[str, int]

class JobTypeSummaryAll(BaseModel):
    total: int
    approved: int
    operating: int
    finished: int

class JobTypeSummaries(BaseModel):
    Exploration: JobTypeSummaryAll
    Development: JobTypeSummaryAll
    Workover: JobTypeSummaryAll
    Well_Service: JobTypeSummaryAll


class JobTypeCounts(BaseModel):
    total: int
    all_approved: int
    operating_and_finished: int
    finished: int

class JobTypeSummaryCard(BaseModel):
    job_type: Dict[str, JobTypeCounts]
    rencana: Dict[str, JobTypeCounts]
    realisasi: Dict[str, JobTypeCounts]
    selesai: Dict[str, JobTypeCounts]

# Opsional: Model untuk respons API jika diperlukan
class JobTypeSummaryResponse(BaseModel):
    job_type_summary: JobTypeSummaryCard


class KKKSJobDataCombined(BaseModel):
    id: str
    name: str
    approved_plans: int
    active_operations: int
    finished_jobs: int
    percentage: float


