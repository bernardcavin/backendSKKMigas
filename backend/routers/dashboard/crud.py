from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from backend.routers.auth.models import *
from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.well.schemas import *
from backend.routers.spatial.models import Area,Lapangan
from backend.routers.spatial.schemas import *
from backend.routers.dashboard.schemas import *
from backend.routers.auth.schemas import GetUser
from backend.routers.well.models import *
from typing import List, Dict
from datetime import date
from sqlalchemy import and_,case,extract,select,text,or_
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
from datetime import date, timedelta
import itertools
from typing import Union
import logging


def count_job_data(db: Session) -> Dict[str, int]:
    operations_count = db.query(func.count(Operation.id)).scalar()
    ppp_count = db.query(func.count(PPP.id)).scalar()
    closeout_count = db.query(func.count(CloseOut.id)).scalar()

    return {
        "job_operations": operations_count,
        "job_ppp": ppp_count,
        "job_closeout": closeout_count
    }

def get_well_names(db: Session) -> List[WellData]:
    try:
        wells = db.query(Well.well_name).all()
        return [WellData(well_name=well.well_name) for well in wells]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in wells: {str(e)}")

def get_job_data(db: Session) -> List[JobData]:
    try:
        jobs = db.query(Job.start_date).all()
        return [JobData(start_date=job.start_date) for job in jobs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in jobs: {str(e)}")

def get_combined_data(db: Session) -> List[Dict]:
    try:
        # Query untuk mendapatkan semua well names
        wells = db.query(Well.id, Well.well_name).all()
        
        # Query untuk mendapatkan semua job plans dengan status dan date_proposed
        job_plans = db.query(Planning.id, Planning.proposed_job_id, Planning.date_proposed, Planning.status).all()
        
        # Query untuk mendapatkan semua jobs dengan start_date dan end_date
        jobs = db.query(Job.id, Job.start_date, Job.end_date, Job.field_id).all()
        
        # Membuat dictionary untuk mempercepat lookup
        well_dict = {w.id: w.well_name for w in wells}
        job_plan_dict = {jp.proposed_job_id: (jp.id, jp.date_proposed, jp.status) for jp in job_plans}
        
        # Menggabungkan data
        combined_data = []
        for job in jobs:
            well_name = None
            job_plan_id = None
            date_proposed = None
            plan_status = None
            
            # Mendapatkan job plan id, date_proposed, dan status
            if job.id in job_plan_dict:
                job_plan_id, date_proposed, plan_status = job_plan_dict[job.id]
            
            # Mencari well_name yang sesuai
            if job.field_id:
                well = db.query(Well).filter(Well.field_id == job.field_id).first()
                if well:
                    well_name = well.well_name
            
            combined_data.append({
                "well_name": well_name,
                "job_plan_id": job_plan_id,
                "job_start_date": job.start_date,
                "job_end_date": job.end_date,
                "plan_date_proposed": date_proposed,
                "plan_status": plan_status
            })
        
        return combined_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Penggunaan fungsi
def get_all_data(db: Session):
    return get_combined_data(db)


# AMBIL DATA KKS ITUNG PERSENTASE DASHBOARD SKK
def get_kkks_job_data(db: Session) -> List[Dict]:
    job_types = ['exploration', 'development', 'workover', 'wellservice']

    query = db.query(
        KKKS.id,
        KKKS.nama_kkks,
        Job.job_type,
        func.count(Planning.id).filter(Planning.status == PlanningStatus.APPROVED).label('approved_plans'),
        func.count(Operation.id).filter(Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])).label('active_operations')
    ).outerjoin(Job, KKKS.id == Job.kkks_id) \
     .outerjoin(Planning, Job.id == Planning.proposed_job_id) \
     .outerjoin(Operation, Planning.id == Operation.job_plan_id) \
     .group_by(KKKS.id, KKKS.nama_kkks, Job.job_type)

    results = query.all()

    kkks_data = {}
    for result in results:
        kkks_id = result.id
        job_type = result.job_type
        if kkks_id not in kkks_data:
            kkks_data[kkks_id] = {
                "id": kkks_id,
                "nama_kkks": result.nama_kkks
            }
        
        approved_plans = result.approved_plans or 0
        active_operations = result.active_operations or 0
        
        percentage = (active_operations / approved_plans * 100) if approved_plans > 0 else 0
        
        kkks_data[kkks_id][job_type] = {
            "approved_plans": approved_plans,
            "active_operations": active_operations,
            "percentage": round(percentage, 2)
        }

    # Ensure all job types are present for each KKKS
    for kkks in kkks_data.values():
        for job_type in job_types:
            if job_type not in kkks:
                kkks[job_type] = {"approved_plans": 0, "active_operations": 0, "percentage": 0}

    return list(kkks_data.values())
# DASHBOARD BAGIAN ATAS YANG ADA PANAH HIJAU
def get_aggregate_job_data(db: Session) -> Dict:
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    
    query = db.query(
        *[func.count(case((Job.job_type == job_type, 1))).label(f'{job_type}_total') for job_type in job_types],
        *[func.count(case((and_(Job.job_type == job_type, Planning.status == PlanningStatus.APPROVED), 1))).label(f'{job_type}_plan') for job_type in job_types],
        *[func.count(case((and_(Job.job_type == job_type, Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])), 1))).label(f'{job_type}_realization') for job_type in job_types]
    ).outerjoin(Planning, Job.id == Planning.proposed_job_id) \
     .outerjoin(Operation, Job.id == Operation.post_operation_job_id)

    result = query.first()

    processed_result = {}
    for job_type in job_types:
        total = getattr(result, f'{job_type}_total')
        plan = getattr(result, f'{job_type}_plan')
        realization = getattr(result, f'{job_type}_realization')
        percentage = (realization / plan * 100) if plan > 0 else 0
        
        processed_result[job_type] = {
            "total": total,
            "plan": plan,
            "realization": realization,
            "percentage": round(percentage, 2)
        }

    return processed_result


def get_job_data_change(db: Session) -> Dict:
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    def get_data_for_date(target_date):
        return db.query(
            *[func.count(case((and_(Job.job_type == job_type, 
                                    Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]),
                                    func.date(Operation.date_started) <= target_date), 1))).label(f'{job_type}_realization') 
              for job_type in job_types]
        ).outerjoin(Operation, Job.id == Operation.post_operation_job_id).first()

    today_data = get_data_for_date(today)
    yesterday_data = get_data_for_date(yesterday)

    changes = {}
    for job_type in job_types:
        today_count = getattr(today_data, f'{job_type}_realization')
        yesterday_count = getattr(yesterday_data, f'{job_type}_realization')
        change = today_count - yesterday_count
        changes[job_type] = change

    return changes


# BAR PALING ATAS DASHBOARD SKK
def generate_job_summary_chart_data_json(db: Session) -> Dict:
    aggregate_data = get_aggregate_job_data(db)
    changes = get_job_data_change(db)

    job_types = list(aggregate_data.keys())
    
    data = [
        {
            "x": job_types,
            "y": [aggregate_data[job_type]["plan"] for job_type in job_types],
            "type": "bar",
            "name": "Rencana",
            "marker": {"color": "rgba(55, 83, 109, 0.7)"}
        },
        {
            "x": job_types,
            "y": [aggregate_data[job_type]["realization"] for job_type in job_types],
            "type": "bar",
            "name": "Realisasi",
            "marker": {"color": "rgba(26, 118, 255, 0.7)"}
        }
    ]

    annotations = []
    for i, job_type in enumerate(job_types):
        change = changes.get(job_type, 0)
        if change != 0:
            annotations.append({
                "x": job_type,
                "y": aggregate_data[job_type]["realization"],
                "text": f"{change:+d}",
                "showarrow": True,
                "arrowhead": 4,
                "arrowsize": 0.5,
                "arrowcolor": "green" if change > 0 else "red",
                "ax": 0,
                "ay": -40 if change > 0 else 40
            })

    layout = {
        "title": "Perbandingan Rencana dan Realisasi per Jenis Pekerjaan",
        "xaxis": {"title": "Jenis Pekerjaan"},
        "yaxis": {"title": "Jumlah"},
        "barmode": "group",
        "annotations": annotations
    }

    return {"data": data, "layout": layout}

# Ini DATA COUNT CARD SKK
def get_job_type_summary(db: Session) -> List[Dict]:
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    
    summary = []
    for job_type in job_types:
        total = db.query(Job).filter(Job.job_type == job_type).count()
        print("initotal",total)
        rencana = db.query(Job).join(Planning).filter(
            Job.job_type == job_type,
            Planning.status == PlanningStatus.APPROVED
        ).count()
        print(rencana)
        realisasi = db.query(Job).join(Operation).filter(
            Job.job_type == job_type,
            Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])
        ).count()
        selesai = db.query(Job).join(Operation).filter(
            Job.job_type == job_type,
            Operation.status == OperationStatus.FINISHED
        ).count()
        
        summary.append({
            "job_type": job_type,
            "total": total,
            "rencana": rencana,
            "realisasi": realisasi,
            "selesai": selesai
        })
    
    return summary


# Graphic dibawah CARD SKK
def get_job_monthly_data_with_cumulative(db: Session) -> Dict:
    current_year = datetime.now().year
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    
    def get_data_for_job_type(job_type):
        # Query for planned jobs
        planned_query = db.query(
            extract('month', Planning.date_proposed).label('month'),
            func.count().label('count')
        ).join(Job).filter(
            Job.job_type == job_type,
            Planning.status == 'APPROVED',
            extract('year', Planning.date_proposed) == current_year
        ).group_by('month')

        # Query for realized jobs
        realized_query = db.query(
            extract('month', Operation.date_started).label('month'),
            func.count().label('count')
        ).join(Job).filter(
            Job.job_type == job_type,
            Operation.status.in_(['OPERATING', 'FINISHED']),
            extract('year', Operation.date_started) == current_year
        ).group_by('month')

        planned_data = {r.month: r.count for r in planned_query.all()}
        realized_data = {r.month: r.count for r in realized_query.all()}

        return planned_data, realized_data

    result = {}
    for job_type in job_types:
        planned_data, realized_data = get_data_for_job_type(job_type)
        
        planned_counts = [planned_data.get(month, 0) for month in range(1, 13)]
        realized_counts = [realized_data.get(month, 0) for month in range(1, 13)]
        
        cumulative_planned = list(itertools.accumulate(planned_counts))
        cumulative_realized = list(itertools.accumulate(realized_counts))

        result[job_type] = {
            "planned": planned_counts,
            "realized": realized_counts,
            "cumulative_planned": cumulative_planned,
            "cumulative_realized": cumulative_realized
        }

    months = [datetime(current_year, month, 1).strftime('%b') for month in range(1, 13)]

    return {
        "months": months,
        "data": result
    }
# Sambungan ATAS
def generate_job_chart_data(db: Session) -> Dict:
    data = get_job_monthly_data_with_cumulative(db)
    
    charts = {}
    for job_type, job_data in data['data'].items():
        charts[job_type] = {
            "data": [
                {
                    "x": data["months"],
                    "y": job_data["planned"],
                    "type": "bar",
                    "name": "Rencana",
                    "marker": {"color": "rgba(55, 83, 109, 0.7)"}
                },
                {
                    "x": data["months"],
                    "y": job_data["realized"],
                    "type": "bar",
                    "name": "Realisasi",
                    "marker": {"color": "rgba(26, 118, 255, 0.7)"}
                },
                {
                    "x": data["months"],
                    "y": job_data["cumulative_planned"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Kumulatif Rencana",
                    "line": {"color": "rgb(255, 127, 14)"}
                },
                {
                    "x": data["months"],
                    "y": job_data["cumulative_realized"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Kumulatif Realisasi",
                    "line": {"color": "rgb(44, 160, 44)"}
                }
            ],
            "layout": {
                "title": f"Realisasi Kegiatan {job_type.capitalize()} Tahun {datetime.now().year}",
                "xaxis": {"title": "Bulan"},
                "yaxis": {"title": "Jumlah"},
                "barmode": "group",
                "yaxis2": {
                    "title": "Kumulatif",
                    "overlaying": "y",
                    "side": "right"
                }
            }
        }
    
    return charts

# PLAN VS ACTUAL COST
def get_budget_summary_by_job_type(db: Session) -> Dict[str, Dict]:
    job_types = ['exploration', 'development', 'workover', 'wellservice']

    # Query untuk planned budget
    planned_budget_query = db.query(
        Job.job_type,
        func.sum(Job.total_budget).label('total')
    ).join(Planning).filter(
        Planning.status == PlanningStatus.APPROVED
    ).group_by(Job.job_type)

    # Query untuk actual budget
    actual_budget_query = db.query(
        Job.job_type,
        func.sum(Job.total_budget).label('total')
    ).join(Operation).filter(
        Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])
    ).group_by(Job.job_type)

    # Convert query results to dictionaries
    planned_budget = {row.job_type: float(row.total) for row in planned_budget_query}
    actual_budget = {row.job_type: float(row.total) for row in actual_budget_query}

    # Prepare the result
    result = {}
    for job_type in job_types:
        result[job_type] = {
            "planned": planned_budget.get(job_type, 0),
            "actual": actual_budget.get(job_type, 0)
        }

    return result

def get_job_and_well_status_summary(db: Session) -> Dict:
    # Count jobs with POST_OPERATION instance type
    post_operation_count = db.query(func.count(Job.id)).filter(
        Job.job_instance_type == JobInstanceType.POST_OPERATION
    ).scalar()

    # Count wells by status
    well_status_counts = db.query(
        Well.well_status,
        func.count(Well.id).label('count')
    ).filter(Well.well_instance_type == WellInstanceType.POST_OPERATION).group_by(Well.well_status).all()

    # Prepare well status data
    well_status_data = {status.value: count for status, count in well_status_counts}

    # Combine data
    summary = {
        "post_operation_count": post_operation_count,
        "well_status": well_status_data
    }

    print(well_status_counts)

    return summary

# DATA PALING BAWAH TABLE REALISASI KEGIATAN SETIAP KKKS

def calculate_exploration_realization(db: Session) -> List[ExplorationRealizationItem]:
    """
    Calculate the realization percentage of exploration activities for each KKKS.
    
    :param db: Database session
    :return: List of ExplorationRealizationItem objects
    """
    results = (
        db.query(
            KKKS.id.label('kkks_id'),
            KKKS.nama_kkks.label('kkks_name'),
            func.count(case((Planning.status == PlanningStatus.APPROVED, Planning.id))).label('approved_plans'),
            func.count(case((Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Operation.id))).label('completed_operations')
        )
        .join(Job, KKKS.id == Job.kkks_id)
        .join(Exploration, Job.id == Exploration.id)
        .outerjoin(Planning, Job.id == Planning.proposed_job_id)
        .outerjoin(Operation, Job.id == Operation.post_operation_job_id)
        .group_by(KKKS.id, KKKS.nama_kkks)
        .all()
    )

    realization_data = []
    for result in results:
        realization_percentage = (result.completed_operations / result.approved_plans * 100) if result.approved_plans > 0 else 0
        realization_data.append(ExplorationRealizationItem(
            kkks_id=result.kkks_id,
            kkks_name=result.kkks_name,
            approved_plans=result.approved_plans,
            completed_operations=result.completed_operations,
            realization_percentage=round(realization_percentage, 2)
        ))
    print(realization_data)

    return realization_data



def get_kkks_job_counts(db: Session, kkks_id: str):
    query = (
        select(
            func.count(Job.id).label('total_jobs'),
            func.sum(case((Planning.status == PlanningStatus.APPROVED, 1), else_=0)).label('approved_jobs'),
            func.sum(case((Operation.status == OperationStatus.OPERATING, 1), else_=0)).label('operating_jobs'),
            func.sum(case((Operation.status == OperationStatus.FINISHED, 1), else_=0)).label('finished_jobs')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, Job.id == Planning.proposed_job_id)
        .outerjoin(Operation, Job.id == Operation.post_operation_job_id)
        .filter(KKKS.id == kkks_id)
    )
    return db.execute(query).first()

def get_kkks_monthly_data(db: Session, kkks_id: str):
    current_year = datetime.now().year
    
    query = (
        select(
            func.strftime('%Y-%m', Job.start_date).label('month'),
            func.count(Planning.id).label('planned_count'),
            func.count(Operation.id).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, (Job.id == Planning.proposed_job_id) & (Planning.status == PlanningStatus.APPROVED))
        .outerjoin(Operation, (Job.id == Operation.post_operation_job_id) & 
                   (Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])))
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.start_date) == str(current_year))
        .group_by(func.strftime('%Y-%m', Job.start_date))
    )
    
    results = {row.month: {'planned': row.planned_count, 'realized': row.realized_count} for row in db.execute(query)}
    
    all_months = [f"{current_year}-{month:02d}" for month in range(1, 13)]
    return [
        TimeSeriesData(
            time_period=month,
            planned=results.get(month, {}).get('planned', 0),
            realized=results.get(month, {}).get('realized', 0)
        ) for month in all_months
    ]

def get_kkks_weekly_data(db: Session, kkks_id: str):
    current_year = datetime.now().year
    
    query = (
        select(
            func.strftime('%Y-%W', Job.start_date).label('week'),
            func.count(Planning.id).label('planned_count'),
            func.count(Operation.id).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, (Job.id == Planning.proposed_job_id) & (Planning.status == PlanningStatus.APPROVED))
        .outerjoin(Operation, (Job.id == Operation.post_operation_job_id) & 
                   (Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])))
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.start_date) == str(current_year))
        .group_by(func.strftime('%Y-%W', Job.start_date))
    )
    
    results = {row.week: {'planned': row.planned_count, 'realized': row.realized_count} for row in db.execute(query)}
    
    all_weeks = [f"{current_year}-{week:02d}" for week in range(1, 54)]  # Up to 53 weeks
    return [
        TimeSeriesData(
            time_period=week,
            planned=results.get(week, {}).get('planned', 0),
            realized=results.get(week, {}).get('realized', 0)
        ) for week in all_weeks
    ]

def create_charts(monthly_data: List[TimeSeriesData], weekly_data: List[TimeSeriesData], kkks_name: str):
    chart_data = {
        "data": [
            {
                "type": "bar",
                "name": "Monthly Planned",
                "x": [item.time_period for item in monthly_data],
                "y": [item.planned for item in monthly_data],
                "marker": {"color": "blue"},
            },
            {
                "type": "bar",
                "name": "Monthly Realized",
                "x": [item.time_period for item in monthly_data],
                "y": [item.realized for item in monthly_data],
                "marker": {"color": "red"},
            },
            {
                "type": "bar",
                "name": "Weekly Planned",
                "x": [item.time_period for item in weekly_data],
                "y": [item.planned for item in weekly_data],
                "marker": {"color": "blue"},
                "xaxis": "x2",
                "yaxis": "y2",
            },
            {
                "type": "bar",
                "name": "Weekly Realized",
                "x": [item.time_period for item in weekly_data],
                "y": [item.realized for item in weekly_data],
                "marker": {"color": "red"},
                "xaxis": "x2",
                "yaxis": "y2",
            },
        ],
        "layout": {
            "title": f"KKKS: {kkks_name} - Job Data",
            "height": 1000,
            "grid": {"rows": 2, "columns": 1, "pattern": "independent"},
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Number of Jobs"},
            "xaxis2": {"title": "Week"},
            "yaxis2": {"title": "Number of Jobs"},
        },
    }
    return json.dumps(chart_data)

# Import your database models and session dependency


router = APIRouter()


def get_kkks_job_counts(db: Session, kkks_id: str):
    query = (
        select(
            func.count(Job.id).label('total_jobs'),
            func.sum(case((Planning.status == PlanningStatus.APPROVED, 1), else_=0)).label('approved_jobs'),
            func.sum(case((Operation.status == OperationStatus.OPERATING, 1), else_=0)).label('operating_jobs'),
            func.sum(case((Operation.status == OperationStatus.FINISHED, 1), else_=0)).label('finished_jobs')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, Job.id == Planning.proposed_job_id)
        .outerjoin(Operation, Job.id == Operation.post_operation_job_id)
        .filter(KKKS.id == kkks_id)
    )
    return db.execute(query).first()

def get_kkks_monthly_data(db: Session, kkks_id: str):
    current_year = datetime.now().year
    
    query = (
        select(
            func.strftime('%Y-%m', Job.start_date).label('month'),
            func.count(Planning.id).label('planned_count'),
            func.count(Operation.id).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, (Job.id == Planning.proposed_job_id) & (Planning.status == PlanningStatus.APPROVED))
        .outerjoin(Operation, (Job.id == Operation.post_operation_job_id) & 
                   (Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])))
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.start_date) == str(current_year))
        .group_by(func.strftime('%Y-%m', Job.start_date))
    )
    
    results = {row.month: {'planned': row.planned_count, 'realized': row.realized_count} for row in db.execute(query)}
    
    all_months = [f"{current_year}-{month:02d}" for month in range(1, 13)]
    return [
        TimeSeriesData(
            time_period=month,
            planned=results.get(month, {}).get('planned', 0),
            realized=results.get(month, {}).get('realized', 0)
        ) for month in all_months
    ]

def get_kkks_weekly_data(db: Session, kkks_id: str):
    current_year = datetime.now().year
    
    query = (
        select(
            func.strftime('%Y-%W', Job.start_date).label('week'),
            func.count(Planning.id).label('planned_count'),
            func.count(Operation.id).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .outerjoin(Planning, (Job.id == Planning.proposed_job_id) & (Planning.status == PlanningStatus.APPROVED))
        .outerjoin(Operation, (Job.id == Operation.post_operation_job_id) & 
                   (Operation.status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])))
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.start_date) == str(current_year))
        .group_by(func.strftime('%Y-%W', Job.start_date))
    )
    
    results = {row.week: {'planned': row.planned_count, 'realized': row.realized_count} for row in db.execute(query)}
    
    all_weeks = [f"{current_year}-{week:02d}" for week in range(1, 54)]  # Up to 53 weeks
    return [
        TimeSeriesData(
            time_period=week,
            planned=results.get(week, {}).get('planned', 0),
            realized=results.get(week, {}).get('realized', 0)
        ) for week in all_weeks
    ]

def create_charts(monthly_data: List[TimeSeriesData], weekly_data: List[TimeSeriesData], kkks_name: str):
    chart_data = {
        "data": [
            {
                "type": "bar",
                "name": "Monthly Planned",
                "x": [item.time_period for item in monthly_data],
                "y": [item.planned for item in monthly_data],
                "marker": {"color": "blue"},
            },
            {
                "type": "bar",
                "name": "Monthly Realized",
                "x": [item.time_period for item in monthly_data],
                "y": [item.realized for item in monthly_data],
                "marker": {"color": "red"},
            },
            {
                "type": "bar",
                "name": "Weekly Planned",
                "x": [item.time_period for item in weekly_data],
                "y": [item.planned for item in weekly_data],
                "marker": {"color": "blue"},
                "xaxis": "x2",
                "yaxis": "y2",
            },
            {
                "type": "bar",
                "name": "Weekly Realized",
                "x": [item.time_period for item in weekly_data],
                "y": [item.realized for item in weekly_data],
                "marker": {"color": "red"},
                "xaxis": "x2",
                "yaxis": "y2",
            },
        ],
        "layout": {
            "title": f"KKKS: {kkks_name} - Job Data",
            "height": 1000,
            "grid": {"rows": 2, "columns": 1, "pattern": "independent"},
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Number of Jobs"},
            "xaxis2": {"title": "Week"},
            "yaxis2": {"title": "Number of Jobs"},
        },
    }
    return json.dumps(chart_data)

def get_well_job_data(db: Session, kkks_id: str):
    query = (
        select(
            Well.well_name,
            Area.area_name.label('wilayah_kerja'),
            Lapangan.field_name.label('lapangan'),
            Job.start_date.label('tanggal_mulai'),
            Job.end_date.label('tanggal_selesai'),
            Operation.date_started.label('tanggal_realisasi'),
            Planning.status.label('plan_status'),
            Operation.status.label('operation_status')
        )
        .select_from(Well)
        .join(Area, Well.area_id == Area.id)
        .join(Lapangan, Well.field_id == Lapangan.id)
        .join(Job, Well.kkks_id == Job.kkks_id)
        .outerjoin(Planning, (Job.id == Planning.proposed_job_id) & (Planning.status == PlanningStatus.APPROVED))
        .outerjoin(Operation, (Job.id == Operation.post_operation_job_id) & 
                   (Operation.status == OperationStatus.OPERATING))
        .where(Well.kkks_id == kkks_id)
        .where(or_(Planning.status == PlanningStatus.APPROVED, Operation.status == OperationStatus.OPERATING))
    )

    results = db.execute(query).all()

    return [
        WellJobData(
            nama_sumur=row.well_name,
            wilayah_kerja=row.wilayah_kerja,
            lapangan=row.lapangan if row.lapangan else None,
            tanggal_mulai=row.tanggal_mulai.strftime('%d %B %Y') if row.tanggal_mulai else None,
            tanggal_selesai=row.tanggal_selesai.strftime('%d %B %Y') if row.tanggal_selesai else None,
            tanggal_realisasi=row.tanggal_realisasi.strftime('%d %B %Y') if row.tanggal_realisasi else None,
            status="APPROVED" if row.plan_status == PlanningStatus.APPROVED else "OPERATING"
        ) for row in results
    ]

def get_job_counts(db: Session, job_types: List[str], statuses: List[str]) -> List[JobCountResponse]:
    try:
        # Query untuk menghitung jumlah berdasarkan job_type dan status
        query = (
            db.query(
                Job.job_type,
                Planning.status,
                func.count().label('count')
            )
            .join(Planning, Job.id == Planning.proposed_job_id)
            .filter(Job.job_type.in_(job_types), Planning.status.in_(statuses))
            .group_by(Job.job_type, Planning.status)
        )
        
        results = query.all()
       

        if not results:
            return []

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
        # Log exception atau handle sesuai kebutuhan
        raise