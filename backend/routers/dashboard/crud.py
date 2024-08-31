from unittest import result
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
from backend.routers.dashboard.models import *
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
from collections import defaultdict


def count_job_data(db: Session) -> Dict[str, int]:
    operations_count = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DEVELOPMENT).scalar()
    ppp_count = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WORKOVER).scalar()
    closeout_count = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WELLSERVICE).scalar()

    return {
        "job_operations": operations_count,
        "job_ppp": ppp_count,
        "job_closeout": closeout_count
    }


def get_well_names(db: Session) -> List[WellData]:
    try:
        wells = db.query(WellInstance.well_name).all()
        return [WellData(well_name=well.well_name) for well in wells]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in wells: {str(e)}")

def get_job_data(db: Session) -> List[JobData]:
    try:
        jobs = db.query(Job.start_date).all()
        return [JobData(start_date=job.start_date) for job in jobs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in jobs: {str(e)}")

def get_status_counts(db: Session) -> List[Dict[str, Any]]:
    try:
        # Query to get well names along with relevant status counts and dates
        results = (
            db.query(
                WellInstance.well_name.label('well_name'),
                WellInstance.well_name.label('well_name'),
                func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).label('approved_planning_count'),
                func.count(Job.id).filter(Job.operation_status == OperationStatus.OPERATING).label('operating_count'),
                func.count(Job.id).filter(Job.operation_status == OperationStatus.FINISHED).label('finished_count'),
                func.count(Job.id).filter(Job.ppp_status == PPPStatus.APPROVED).label('approved_ppp_count'),
                func.count(Job.id).filter(Job.closeout_status == CloseOutStatus.APPROVED).label('approved_closeout_count'),
                func.min(Job.planning_status).label('planning_status'),
                func.min(Job.date_approved).label('date_approved'),
                func.min(Job.date_proposed).label('date_proposed'),
                func.min(Job.date_returned).label('date_returned'),
                func.min(Job.date_started).label('date_started'),
                func.max(Job.date_finished).label('date_finished'),
                func.min(Job.operation_status).label('operation_status'),
                func.min(Job.date_ppp_proposed).label('date_ppp_proposed'),
                func.min(Job.date_ppp_approved).label('date_ppp_approved'),
                func.min(Job.ppp_status).label('ppp_status'),
                func.min(Job.closeout_status).label('closeout_status')
            )
            .join(Job, (Job.field_id == WellInstance.field_id))
            .group_by(WellInstance.well_name)
            .join(Job, (Job.field_id == WellInstance.field_id))
            .group_by(WellInstance.well_name)
            .all()
        )

        print(results)

        # Convert the results into a list of dictionaries
        data = [
            {
                "well_name": r.well_name,
                "approved_planning_count": r.approved_planning_count,
                "operating_count": r.operating_count,
                "finished_count": r.finished_count,
                "approved_ppp_count": r.approved_ppp_count,
                "approved_closeout_count": r.approved_closeout_count,
                "planning_status": r.planning_status.value if r.planning_status else None,
                "date_approved": r.date_approved,
                "date_proposed": r.date_proposed,
                "date_returned": r.date_returned,
                "date_started": r.date_started,
                "date_finished": r.date_finished,
                "operation_status": r.operation_status.value if r.operation_status else None,
                "date_ppp_proposed": r.date_ppp_proposed,
                "date_ppp_approved": r.date_ppp_approved,
                "ppp_status": r.ppp_status.value if r.ppp_status else None,
                "closeout_status": r.closeout_status.value if r.closeout_status else None
            }
            for r in results
        ]

        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


# # Penggunaan fungsi
# def get_all_data(db: Session):
#     return get_combined_data(db)


# AMBIL DATA KKS ITUNG PERSENTASE DASHBOARD SKK
def get_kkks_job_data(db: Session) -> List[Dict]:
    job_types = ['exploration', 'development', 'workover', 'wellservice']

    query = db.query(
        KKKS.id,
        KKKS.nama_kkks.label('nama_kkks'),
        Job.job_type,
        func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).label('approved_plans'),
        func.count(Job.id).filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])).label('active_operations')
    ).outerjoin(Job, KKKS.id == Job.kkks_id) \
     .group_by(KKKS.id, KKKS.nama_kkks, Job.job_type)

    results = query.all()

    kkks_data = {}
    for result in results:
        kkks_id = result.id
        job_type = result.job_type.value.lower() if result.job_type else None
        if kkks_id not in kkks_data:
            kkks_data[kkks_id] = {
                "id": kkks_id,
                "nama_kkks": result.nama_kkks
            }
            for jt in job_types:
                kkks_data[kkks_id][jt] = {
                    "approved_plans": 0,
                    "active_operations": 0,
                    "percentage": 0
                }

        if job_type in job_types:
            approved_plans = result.approved_plans or 0
            active_operations = result.active_operations or 0
            percentage = (active_operations / approved_plans * 100) if approved_plans > 0 else 0

            kkks_data[kkks_id][job_type] = {
                "approved_plans": approved_plans,
                "active_operations": active_operations,
                "percentage": round(percentage, 2)
            }

    return list(kkks_data.values())
# DASHBOARD BAGIAN ATAS YANG ADA PANAH HIJAU
def get_job_data_change(db: Session) -> Dict:
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    today = date.today()
    yesterday = today - timedelta(days=1)

    def get_data_for_date(target_date):
        return db.query(
            *[func.count(case((and_(
                Job.job_type == (JobType.WELLSERVICE if job_type == 'wellservice' else JobType[job_type.upper()]),
                Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]),
                func.date(Job.date_started) <= target_date
            ), 1))).label(f'{job_type}_realization')
              for job_type in job_types]
        ).first()

    today_data = get_data_for_date(today)
    yesterday_data = get_data_for_date(yesterday)

    changes = {}
    for job_type in job_types:
        today_count = getattr(today_data, f'{job_type}_realization')
        yesterday_count = getattr(yesterday_data, f'{job_type}_realization')
        change = today_count - yesterday_count
        changes[job_type] = change

    return changes
def get_aggregate_job_data(db: Session) -> Dict:
    job_types = [job_type.value.lower() for job_type in JobType]
    
    results = db.query(
        Job.job_type,
        func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).label('plan'),
        func.count(Job.id).filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])).label('realization')
    ).group_by(Job.job_type).all()

    aggregate_data = {job_type: {"plan": 0, "realization": 0} for job_type in job_types}
    
    for result in results:
        job_type = result.job_type.value.lower()
        aggregate_data[job_type]["plan"] = result.plan
        aggregate_data[job_type]["realization"] = result.realization

    return aggregate_data

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
        job_type_enum = JobType.WELLSERVICE if job_type == 'wellservice' else JobType[job_type.upper()]
        
        total = db.query(Job).filter(Job.job_type == job_type_enum).count()
        print("initotal", total)
        
        rencana = db.query(Job).filter(
            Job.job_type == job_type_enum,
            Job.planning_status == PlanningStatus.APPROVED
        ).count()
        print(rencana)
        
        realisasi = db.query(Job).filter(
            Job.job_type == job_type_enum,
            Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])
        ).count()
        
        selesai = db.query(Job).filter(
            Job.job_type == job_type_enum,
            Job.operation_status == OperationStatus.FINISHED
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
        job_type_enum = JobType.WELLSERVICE if job_type == 'wellservice' else JobType[job_type.upper()]
        
        # Query for planned jobs
        planned_query = db.query(
            extract('month', Job.date_proposed).label('month'),
            func.count().label('count')
        ).filter(
            Job.job_type == job_type_enum,
            Job.planning_status == PlanningStatus.APPROVED,
            extract('year', Job.date_proposed) == current_year
        ).group_by('month')

        # Query for realized jobs
        realized_query = db.query(
            extract('month', Job.date_started).label('month'),
            func.count().label('count')
        ).filter(
            Job.job_type == job_type_enum,
            Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]),
            extract('year', Job.date_started) == current_year
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
    job_types = [job_type.value for job_type in JobType]

    # Query for planned budget
    planned_budget_query = db.query(
        JobInstance.job_type,
        func.sum(JobInstance.total_budget).label('total')
    ).join(
        Job, Job.job_plan_id == JobInstance.id
    ).filter(
        Job.planning_status == PlanningStatus.APPROVED
    ).group_by(JobInstance.job_type)

    # Query for actual budget
    actual_budget_query = db.query(
        JobInstance.job_type,
        func.sum(JobInstance.total_budget).label('total')
    ).join(
        Job, Job.actual_job_id == JobInstance.id
    ).filter(
        Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])
    ).group_by(JobInstance.job_type)

    # Convert query results to dictionaries
    planned_budget = {row.job_type.value: float(row.total) for row in planned_budget_query}
    actual_budget = {row.job_type.value: float(row.total) for row in actual_budget_query}

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
        WellInstance.well_status,
        func.count(WellInstance.id).label('count')
    ).filter(WellInstance.well_instance_type == WellInstanceType.POST_OPERATION).group_by(WellInstance.well_status).all()
    # Prepare well status data
    well_status_data = {status.value: count for status, count in well_status_counts}

    # Combine data
    summary = {
        "post_operation_count": post_operation_count,
        "well_status": well_status_data
    }

    print(well_status_counts)

    return summary

def calculate_exploration_realization(db: Session) -> List[ExplorationRealizationItem]:
    results = (
        db.query(
            KKKS.id.label('kkks_id'),
            KKKS.name.label('kkks_name'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id))).label('approved_plans'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id))).label('completed_operations')
        )
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(Job.job_type == JobType.EXPLORATION)
        .group_by(KKKS.id, KKKS.name)
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

def get_kkks_monthly_data(db: Session, kkks_id: str):
    current_year = datetime.now().year
    
    query = (
        select(
            func.strftime('%Y-%m', Job.date_proposed).label('month'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id), else_=None)).label('planned_count'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id), else_=None)).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.date_proposed) == str(current_year))
        .group_by(func.strftime('%Y-%m', Job.date_proposed))
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
            func.strftime('%Y-%W', Job.date_proposed).label('week'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id), else_=None)).label('planned_count'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id), else_=None)).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.date_proposed) == str(current_year))
        .group_by(func.strftime('%Y-%W', Job.date_proposed))
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

def get_well_job_data(db: Session, kkks_id: str):
    query = (
        select(
            WellInstance.name.label('well_name'),
            WellInstance.name.label('well_name'),
            Area.name.label('wilayah_kerja'),
            Lapangan.name.label('lapangan'),
            Job.date_proposed.label('tanggal_mulai'),
            Job.date_approved.label('tanggal_selesai'),
            Job.date_started.label('tanggal_realisasi'),
            Job.planning_status.label('plan_status'),
            Job.operation_status.label('operation_status')
        )
        .select_from(WellInstance)
        .join(Area, WellInstance.area_id == Area.id)
        .join(Lapangan, WellInstance.field_id == Lapangan.id)
        .join(Job, WellInstance.kkks_id == Job.kkks_id)
        .where(WellInstance.kkks_id == kkks_id)
        .select_from(WellInstance)
        .join(Area, WellInstance.area_id == Area.id)
        .join(Lapangan, WellInstance.field_id == Lapangan.id)
        .join(Job, WellInstance.kkks_id == Job.kkks_id)
        .where(WellInstance.kkks_id == kkks_id)
        .where(or_(Job.planning_status == PlanningStatus.APPROVED, Job.operation_status == OperationStatus.OPERATING))
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
        query = (
            db.query(
                Job.job_type,
                Job.planning_status,
                func.count().label('count')
            )
            .filter(Job.job_type.in_(job_types), Job.planning_status.in_(statuses))
            .group_by(Job.job_type, Job.planning_status)
        )
        
        results = query.all()
       
        if not results:
            return []

        job_counts = [
            JobCountResponse(
                job_type=job_type.value if job_type else "Unknown",
                status=status.value if status else "Unknown",
                count=count or 0
            )
            for job_type, status, count in results
        ]

        return job_counts

    except Exception as e:
        # Log exception or handle as needed
        raise


def get_job_and_well_status_summary(db: Session) -> Dict:
    # Query jobs grouped by job type and instance type
    job_counts = db.query(
        Job.job_type,
        func.count(Job.id).label('total_count'),
        func.sum(case((Job.job_instance_type == JobInstanceType.POST_OPERATION, 1), else_=0)).label('post_operation_count')
    ).group_by(Job.job_type).all()

    # Prepare job count data
    job_count_data = {}
    for job_type, total_count, post_operation_count in job_counts:
        job_count_data[job_type.value] = {
            "total_count": total_count,
            "post_operation_count": post_operation_count
        }

    # Count wells by status
    well_status_counts = db.query(
        WellInstance.well_status,
        func.count(WellInstance.id).label('count')
    ).group_by(WellInstance.well_status).all()

    # Prepare well status data
    well_status_data = {status.value: count for status, count in well_status_counts}

    # Create Plotly figure
    fig = make_subplots(rows=2, cols=2, specs=[[{'type':'pie'}, {'type':'pie'}],
                                               [{'type':'pie'}, {'type':'pie'}]],
                        subplot_titles=('Total Jobs by Type', 'Post-Operation Jobs by Type',
                                        'Well Status Distribution', ''))

    # Total Jobs Pie Chart
    fig.add_trace(go.Pie(labels=list(job_count_data.keys()),
                         values=[data['total_count'] for data in job_count_data.values()],
                         name="Total Jobs"),
                  row=1, col=1)

    # Post-Operation Jobs Pie Chart
    fig.add_trace(go.Pie(labels=list(job_count_data.keys()),
                         values=[data['post_operation_count'] for data in job_count_data.values()],
                         name="Post-Operation Jobs"),
                  row=1, col=2)

    # Well Status Pie Chart
    fig.add_trace(go.Pie(labels=list(well_status_data.keys()),
                         values=list(well_status_data.values()),
                         name="Well Status"),
                  row=2, col=1)

    # Update layout
    fig.update_layout(height=800, width=800, title_text="Job and Well Status Summary")

    # Convert the figure to a dict and then to JSON
    plot_json = json.dumps(fig.to_dict(), indent=2)

    # Combine data
    summary = {
        "job_counts": job_count_data,
        "well_status": well_status_data,
        "plotly_chart": plot_json
    }

    return summary

def calculate_exploration_realization(db: Session) -> List[ExplorationRealizationItem]:
    results = (
        db.query(
            KKKS.id.label('kkks_id'),
            KKKS.nama_kkks.label('kkks_name'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id))).label('approved_plans'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id))).label('completed_operations')
        )
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(Job.job_type == JobType.EXPLORATION)
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

def get_kkks_monthly_data(db: Session, kkks_id: str) -> Dict[str, List[TimeSeriesData]]:
    current_year = datetime.now().year
    job_types = [job_type.value for job_type in JobType]

    query = (
        select(
            Job.job_type,
            func.strftime('%Y-%m', Job.date_proposed).label('month'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id), else_=None)).label('planned_count'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id), else_=None)).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.date_proposed) == str(current_year))
        .group_by(Job.job_type, func.strftime('%Y-%m', Job.date_proposed))
    )

    results = db.execute(query).fetchall()

    data_by_job_type = {jt: {} for jt in job_types}
    for row in results:
        job_type = row.job_type.value
        month = row.month
        data_by_job_type[job_type][month] = {'planned': row.planned_count, 'realized': row.realized_count}

    all_months = [f"{current_year}-{month:02d}" for month in range(1, 13)]
    
    return {
        job_type: [
            TimeSeriesData(
                time_period=month,
                planned=data_by_job_type[job_type].get(month, {}).get('planned', 0),
                realized=data_by_job_type[job_type].get(month, {}).get('realized', 0)
            ) for month in all_months
        ] for job_type in job_types
    }

def get_kkks_weekly_data(db: Session, kkks_id: str) -> Dict[str, List[TimeSeriesData]]:
    current_year = datetime.now().year
    job_types = [job_type.value for job_type in JobType]

    query = (
        select(
            Job.job_type,
            func.strftime('%Y-%W', Job.date_proposed).label('week'),
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id), else_=None)).label('planned_count'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id), else_=None)).label('realized_count')
        )
        .select_from(KKKS)
        .join(Job, KKKS.id == Job.kkks_id)
        .filter(KKKS.id == kkks_id, func.strftime('%Y', Job.date_proposed) == str(current_year))
        .group_by(Job.job_type, func.strftime('%Y-%W', Job.date_proposed))
    )

    results = db.execute(query).fetchall()

    data_by_job_type = {jt: {} for jt in job_types}
    for row in results:
        job_type = row.job_type.value
        week = row.week
        data_by_job_type[job_type][week] = {'planned': row.planned_count, 'realized': row.realized_count}

    all_weeks = [f"{current_year}-{week:02d}" for week in range(1, 54)]  # Up to 53 weeks
    
    return {
        job_type: [
            TimeSeriesData(
                time_period=week,
                planned=data_by_job_type[job_type].get(week, {}).get('planned', 0),
                realized=data_by_job_type[job_type].get(week, {}).get('realized', 0)
            ) for week in all_weeks
        ] for job_type in job_types
    }
def get_well_job_data(db: Session, kkks_id: str) -> Dict[str, List[WellJobData]]:
    query = (
        select(
            WellInstance.well_name.label('well_name'),
            Area.area_name.label('wilayah_kerja'),
            Lapangan.field_name.label('lapangan'),
            Job.date_proposed.label('tanggal_mulai'),
            Job.date_approved.label('tanggal_selesai'),
            Job.date_started.label('tanggal_realisasi'),
            Job.planning_status.label('plan_status'),
            Job.operation_status.label('operation_status'),
            Job.job_type
        )
        .select_from(WellInstance)
        .join(Area, WellInstance.area_id == Area.id)
        .join(Lapangan, WellInstance.field_id == Lapangan.id)
        .join(Job, WellInstance.kkks_id == Job.kkks_id) 
        .where(WellInstance.kkks_id == kkks_id)
        .where(or_(Job.planning_status == PlanningStatus.APPROVED, Job.operation_status == OperationStatus.OPERATING))
    )

    results = db.execute(query).all()

    well_job_data = {job_type.value.lower(): [] for job_type in JobType}

    for row in results:
        well_data = WellJobData(
            nama_sumur=row.well_name,
            wilayah_kerja=row.wilayah_kerja,
            lapangan=row.lapangan if row.lapangan else None,
            tanggal_mulai=row.tanggal_mulai.strftime('%d %B %Y') if row.tanggal_mulai else None,
            tanggal_selesai=row.tanggal_selesai.strftime('%d %B %Y') if row.tanggal_selesai else None,
            tanggal_realisasi=row.tanggal_realisasi.strftime('%d %B %Y') if row.tanggal_realisasi else None,
            status="APPROVED" if row.plan_status == PlanningStatus.APPROVED else "OPERATING"
        )
        job_type = row.job_type.value.lower()
        well_job_data[job_type].append(well_data)

    return well_job_data

def create_charts(monthly_data: Dict[str, List[TimeSeriesData]], weekly_data: Dict[str, List[TimeSeriesData]], kkks_name: str):
    chart_data = {}
    
    for job_type in monthly_data.keys():
        monthly = monthly_data[job_type]
        weekly = weekly_data[job_type]
        
        job_type_chart = {
            "data": [
                {
                    "type": "bar",
                    "name": f"{job_type.capitalize()} Monthly Planned",
                    "x": [item.time_period for item in monthly],
                    "y": [item.planned for item in monthly],
                    "marker": {"color": "blue"},
                    "xaxis": "x1",
                    "yaxis": "y1",
                },
                {
                    "type": "bar",
                    "name": f"{job_type.capitalize()} Monthly Realized",
                    "x": [item.time_period for item in monthly],
                    "y": [item.realized for item in monthly],
                    "marker": {"color": "red"},
                    "xaxis": "x1",
                    "yaxis": "y1",
                },
                {
                    "type": "bar",
                    "name": f"{job_type.capitalize()} Weekly Planned",
                    "x": [item.time_period for item in weekly],
                    "y": [item.planned for item in weekly],
                    "marker": {"color": "blue"},
                    "xaxis": "x2",
                    "yaxis": "y2",
                },
                {
                    "type": "bar",
                    "name": f"{job_type.capitalize()} Weekly Realized",
                    "x": [item.time_period for item in weekly],
                    "y": [item.realized for item in weekly],
                    "marker": {"color": "red"},
                    "xaxis": "x2",
                    "yaxis": "y2",
                },
            ],
            "layout": {
                "title": f"KKKS: {kkks_name} - {job_type.capitalize()} Job Data",
                "height": 1000,
                "grid": {"rows": 2, "columns": 1, "pattern": "independent"},
                "xaxis1": {"title": f"{job_type.capitalize()} Month"},
                "yaxis1": {"title": "Number of Jobs"},
                "xaxis2": {"title": f"{job_type.capitalize()} Week"},
                "yaxis2": {"title": "Number of Jobs"}
            }
        }
        
        chart_data[job_type] = job_type_chart
    
    return json.dumps(chart_data)

def get_kkks_job_counts(db: Session, kkks_id: str) -> Dict[str, Dict[str, int]]:
    query = (
        db.query(
            Job.job_type,
            func.count(Job.id).label('total_jobs'),
            func.sum(case((Job.planning_status == PlanningStatus.APPROVED, 1), else_=0)).label('approved_jobs'),
            func.sum(case(
                (Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), 1),
                else_=0
            )).label('realized_jobs'),
            func.sum(case((Job.operation_status == OperationStatus.FINISHED, 1), else_=0)).label('finished_jobs')
        )
        .filter(Job.kkks_id == kkks_id)
        .group_by(Job.job_type)
    )
    
    results = query.all()
    
    # Initialize the dictionary with all job types
    job_counts = {job_type.value.lower(): {
        'total_jobs': 0,
        'approved_jobs': 0,
        'realized_jobs': 0,
        'finished_jobs': 0
    } for job_type in JobType}
    
    # Fill in the actual counts
    for row in results:
        job_type = row.job_type.value.lower()
        job_counts[job_type] = {
            'total_jobs': row.total_jobs,
            'approved_jobs': row.approved_jobs,
            'realized_jobs': row.realized_jobs,
            'finished_jobs': row.finished_jobs
        }
    
    return job_counts
# Additional helper function to get job data for a specific KKKS
def get_kkks_job_data(db: Session, kkks_id: str) -> KKKSJobDataChart:
    kkks = db.query(KKKS).filter(KKKS.id == kkks_id).first()
    if not kkks:
        raise HTTPException(status_code=404, detail="KKKS not found")
    
    job_counts = get_kkks_job_counts(db, kkks_id)
    monthly_data = get_kkks_monthly_data(db, kkks_id)
    weekly_data = get_kkks_weekly_data(db, kkks_id)
    well_job_data = get_well_job_data(db, kkks_id)
    
    chart_json = create_charts(monthly_data, weekly_data, kkks.nama_kkks)
    chart_data = json.loads(chart_json)
    
    # Calculate job type data
    job_type_data: Dict[str, JobTypeData] = {}
    for job_type, counts in job_counts.items():
        approved_plans = counts['approved_jobs']
        realized_jobs = counts['realized_jobs']
        finished_jobs = counts['finished_jobs']
        percentage = (realized_jobs / approved_plans * 100) if approved_plans > 0 else 0
        job_type_data[job_type] = JobTypeData(
            approved_plans=approved_plans,
            active_operations=realized_jobs,
            finished_jobs=finished_jobs,
            percentage=round(percentage, 2)
        )
    
    # Create ChartDataKKKS objects for each job type
    chart_data_kkks = {
        job_type: ChartDataKKKS(
            data=job_chart["data"],
            layout=ChartLayout(
                title=job_chart["layout"]["title"],
                xaxis=ChartAxis(title=job_chart["layout"]["xaxis1"]["title"]),
                yaxis=ChartAxis(title=job_chart["layout"]["yaxis1"]["title"])
            )
        )
        for job_type, job_chart in chart_data.items()
    }
    
    # Helper function to get job type data with a fallback to empty data
    def get_job_type_data(job_type: str) -> JobTypeData:
        return job_type_data.get(job_type, JobTypeData(
            approved_plans=0,
            active_operations=0,
            finished_jobs=0,
            percentage=0
        ))
    
    return KKKSJobDataChart(
        id=kkks.id,
        nama_kkks=kkks.nama_kkks,
        exploration=get_job_type_data('exploration'),
        development=get_job_type_data('development'),
        workover=get_job_type_data('workover'),
        wellservice=get_job_type_data('wellservice'),  # Try 'wellservice'
        monthly_data=monthly_data,
        weekly_data=weekly_data,
        well_job_data=well_job_data,
        chart_data=chart_data_kkks
    )

# Function to get overall dashboard data
def get_dashboard_data(db: Session):
    budget_summary = get_budget_summary_by_job_type(db)
    job_well_status = get_job_and_well_status_summary(db)
    exploration_realization = calculate_exploration_realization(db)

    return {
        "budget_summary": budget_summary,
        "job_well_status": job_well_status,
        "exploration_realization": exploration_realization
    }

# Function to get job counts for specific job types and statuses
def generate_rig_type_pie_chart(db: Session) -> Dict:
    # Query to count rig types
    rig_type_counts = db.query(
        JobInstance.rig_type,
        func.count(JobInstance.id).label('count')
    ).group_by(JobInstance.rig_type).all()

    # Process the results
    labels = []
    values = []
    for rig_type, count in rig_type_counts:
        if rig_type is not None:
            labels.append(rig_type.value)
            values.append(count)

    # Create Plotly figure
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        hoverinfo='label+percent+value',
        textinfo='percent',
        insidetextorientation='radial'
    )])

    fig.update_layout(
        title_text="Rig Type Distribution",
        height=500,
        width=700
    )

    # Convert the figure to JSON
    chart_json = fig.to_json()

    return {
        "chart_data": chart_json,
        "raw_data": {
            "labels": labels,
            "values": values
        }
    }

def get_jobs(db: Session) -> Dict[str, List[Dict]]:
    jobs = db.query(
        Job.id,
        Job.job_type,
        WellInstance.well_name,
        Area.area_name,
        Lapangan.field_name,
        Job.date_proposed,
        Job.date_approved,
        Job.date_started,
        Job.planning_status
    ).join(WellInstance, Job.area_id == WellInstance.area_id)\
     .join(Area, Job.area_id == Area.id)\
     .join(Lapangan, Job.field_id == Lapangan.id)\
     .all()

    result = defaultdict(list)
    for job in jobs:
        job_data = {
            "id": job.id,
            "well_name": job.well_name,
            "area_name": job.area_name,
            "field_name": job.field_name,
            "date_proposed": job.date_proposed.strftime("%d %B %Y") if job.date_proposed else None,
            "date_approved": job.date_approved.strftime("%d %B %Y") if job.date_approved else None,
            "date_started": job.date_started.strftime("%d %B %Y") if job.date_started else None,
            "planning_status": job.planning_status.value
        }
        result[job.job_type.value].append(job_data)
    
    return dict(result)