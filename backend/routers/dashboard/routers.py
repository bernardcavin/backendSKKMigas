from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy import func, extract, and_, cast, Integer,text,or_
from sqlalchemy.orm import Session
from typing import Dict,List
from backend.routers.auth.models import Role
from backend.routers.job.models import *
from backend.routers.well.schemas import *
from backend.routers.well.models import *
from backend.routers.spatial.models import *
from backend.routers.auth.schemas import GetUser
from backend.routers.dashboard.crud import *
from calendar import monthrange, month_name as calendar_month_name
from datetime import datetime,timedelta
import plotly.graph_objects as go
import numpy as np

from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas, models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])



@router.get("/job-counts", response_model=Dict[str, int])
async def get_job_counts(db: Session = Depends(get_db)):
    try:
        counts = count_job_data(db)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/job-well-data", response_model=CombinedData)
async def read_job_and_well_data(db: Session = Depends(get_db)):
    try:
        well_data = get_well_names(db)
        job_data = get_job_data(db)
        return CombinedData(wells=well_data, jobs=job_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/combined-data")
def read_combined_data(db: Session = Depends(get_db)):
    return get_combined_data(db)

@router.get("/kkks-job-data", response_model=List[KKKSJobData])
def read_kkks_job_data(db: Session = Depends(get_db)):
    return get_kkks_job_data(db)

@router.get("/aggregate-job-data", response_model=AggregateJobData)
def read_aggregate_job_data(db: Session = Depends(get_db)):
    aggregate_data = get_aggregate_job_data(db)
    changes = get_job_data_change(db)
    
    result = {}
    for job_type in ['exploration', 'development', 'workover', 'wellservice']:
        data = aggregate_data[job_type]
        result[job_type] = JobTypeDataUP(
            total=data['total'],
            plan=data['plan'],
            realization=data['realization'],
            percentage=data['percentage'],
            change=changes[job_type]
        )
    
    return AggregateJobData(**result)


@router.get("/job-summary-chart", response_model=Dict)
async def get_job_summary_chart(db: Session = Depends(get_db)):
    """
    Endpoint to get job summary chart data for Plotly visualization.
    """
    chart_data = generate_job_summary_chart_data_json(db)
    return chart_data

@router.get("/job-type-summary-skk", response_model=List[JobTypeSummary])
async def read_job_type_summary(db: Session = Depends(get_db)):
    """
    Get summary of job counts for each job type.
    """
    return get_job_type_summary(db)

@router.get("/job-charts", response_model=Dict)
async def get_job_charts(db: Session = Depends(get_db)):
    return generate_job_chart_data(db)

@router.get("/budget-summary-charts", response_model=BudgetSummaryResponse)
async def read_budget_summary_charts(db: Session = Depends(get_db)):
    budget_data = get_budget_summary_by_job_type(db)
    
    charts = {}
    for job_type, data in budget_data.items():
        charts[job_type] = ChartData(
            data=[{
                "y": ["Plan", "Actual"],
                "x": [data["planned"], data["actual"]],
                "type": "bar",
                "orientation": "h",
                "marker": {
                    "color": ["rgba(103, 58, 183, 0.8)", "rgba(156, 39, 176, 0.8)"]
                }
            }],
            layout={
                "title": f"{job_type.capitalize()} Budget",
                "xaxis": {"title": "Budget (million US$)"},
                "height": 400,
                "width": 500,
                "margin": {"l": 100}  # Increase left margin for labels
            }
        )
    
    return BudgetSummaryResponse(charts=charts)

@router.get("/job-well-status-chart", response_model=Dict)
async def read_job_well_status_chart(db: Session = Depends(get_db)):
    data = get_job_and_well_status_summary(db)
    
    labels = list(data['well_status'].keys()) + ['Other Jobs']
    values = list(data['well_status'].values()) + [data['post_operation_count']]

    chart_data = {
        "data": [{
            "labels": labels,
            "values": values,
            "type": "pie",
            "marker": {
                "colors": [
                    "rgba(103, 58, 183, 0.8)",  # Active
                    "rgba(156, 39, 176, 0.8)",  # Suspended
                    "rgba(33, 150, 243, 0.8)",  # Abandoned
                    "rgba(0, 188, 212, 0.8)",   # Abandoned Whipstocked
                    "rgba(76, 175, 80, 0.8)",   # Capped
                    "rgba(255, 235, 59, 0.8)",  # Potential
                    "rgba(255, 152, 0, 0.8)",   # Abandoned Junked
                    "rgba(244, 67, 54, 0.8)",   # Not Drilled
                    "rgba(158, 158, 158, 0.8)", # Cancelled
                    "rgba(96, 125, 139, 0.8)"   # Other Jobs (POST_OPERATION)
                ]
            }
        }],
        "layout": {
            "title": "Status Akhir",
            "height": 500,
            "width": 700
        }
    }
    
    return chart_data


@router.get("/exploration/realization", response_model=ExplorationRealizationResponse)
async def get_exploration_realization(db: Session = Depends(get_db)):
    """
    Get the realization percentage of exploration activities for each KKKS.
    
    :param db: Database session
    :return: ExplorationRealizationResponse object containing a list of realization data
    """
    try:
        realization_data = calculate_exploration_realization(db)
        return ExplorationRealizationResponse(data=realization_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kkks/{kkks_id}/detail", response_model=KKKSDetailResponse)
async def get_kkks_detail(kkks_id: str, db: Session = Depends(get_db)):
    kkks = db.query(KKKS).filter(KKKS.id == kkks_id).first()
    if not kkks:
        raise HTTPException(status_code=404, detail=f"KKKS with id {kkks_id} not found")

    job_counts = get_kkks_job_counts(db, kkks_id)
    monthly_data = get_kkks_monthly_data(db, kkks_id)
    weekly_data = get_kkks_weekly_data(db, kkks_id)
    
    chart_json = create_charts(monthly_data, weekly_data, kkks.nama_kkks)
    well_job_data = get_well_job_data(db, kkks_id)


    return KKKSDetailResponse(
        kkks_name=kkks.nama_kkks,
        total_jobs=job_counts.total_jobs,
        approved_jobs=job_counts.approved_jobs,
        operating_jobs=job_counts.operating_jobs,
        finished_jobs=job_counts.finished_jobs,
        monthly_data=monthly_data,
        weekly_data=weekly_data,
        chart_data=ChartDataModal(chart_json=chart_json),
        well_job_data=well_job_data
    )

@router.get("/job-counts/planning", response_model=List[JobCountResponse])
def job_counts(db: Session = Depends(get_db)):
    try:
        # Default job_types dan statuses
        job_type = ["exploration", "development", "workover","wellservices"]  # Sesuaikan dengan tipe pekerjaan yang ada di database
        statuses = ["Proposed", "Approved", "Returned"]  # Sesuaikan dengan status yang ada di database

        # Query untuk menghitung jumlah berdasarkan job_type dan status
        query = (
            db.query(
                Job.job_type,
                Planning.status,
                func.count().label('count')
            )
            .join(Planning, Job.id == Planning.proposed_job_id)
            .group_by(Job.job_type, Planning.status)
        )
        print(query)
        
        results = query.all()
        print(results)

        if not results:
            raise HTTPException(status_code=404, detail="No data found")

        job_counts = [
            JobCountResponse(
                job_type=job_type or "Unknown",
                status=status or "Unknown",
                count=count or 0
            )
            for job_type, status, count in results
        ]

        return job_counts

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
