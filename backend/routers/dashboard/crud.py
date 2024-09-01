from cProfile import label
from unittest import result
from sqlalchemy.orm import Session,aliased
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
from sqlalchemy import and_,case,extract,select,text,or_,union_all,literal_column
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
from datetime import date, timedelta
import itertools
from typing import Union
import logging
from collections import defaultdict,Counter


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

def get_status_counts_by_job_type(db: Session) -> Dict[str, Dict[str, Any]]:
    try:
        # Query to get well names and job types along with relevant status and dates
        results = (
            db.query(
                Job.job_type.label('job_type'),
                WellInstance.well_name.label('well_name'),
                Area.area_name.label('wilayah_kerja'),
                Lapangan.field_name.label('lapangan'),
                Job.planning_status.label('planning_status'),
                Job.operation_status.label('operation_status'),
                Job.ppp_status.label('ppp_status'),
                Job.closeout_status.label('closeout_status'),
                Job.date_approved.label('date_approved'),
                Job.date_proposed.label('date_proposed'),
                Job.date_returned.label('date_returned'),
                Job.date_started.label('date_started'),
                Job.date_finished.label('date_finished'),
                Job.date_ppp_proposed.label('date_ppp_proposed'),
                Job.date_ppp_approved.label('date_ppp_approved')
            )
            .join(WellInstance, Job.field_id == WellInstance.field_id)
            .join(Area, Job.area_id == Area.id)
            .join(Lapangan, Job.field_id == Lapangan.id)
            .all()
        )

        # Initialize data structure
        data = {}
        
        # Process results and count statuses
        for r in results:
            job_type = r.job_type.value if r.job_type else 'Unknown'
            if job_type not in data:
                data[job_type] = {
                    'wells': [],
                    'planning_status_counts': Counter(),
                    'operation_status_counts': Counter(),
                    'ppp_status_counts': Counter(),
                    'closeout_status_counts': Counter()
                }
            
            # Count statuses
            data[job_type]['planning_status_counts'][r.planning_status.value if r.planning_status else 'None'] += 1
            data[job_type]['operation_status_counts'][r.operation_status.value if r.operation_status else 'None'] += 1
            data[job_type]['ppp_status_counts'][r.ppp_status.value if r.ppp_status else 'None'] += 1
            data[job_type]['closeout_status_counts'][r.closeout_status.value if r.closeout_status else 'None'] += 1

            # Prepare well data
            well_data = {
                "well_name": r.well_name,
                "wilayah_kerja": r.wilayah_kerja,
                "lapangan": r.lapangan,
                "planning_status": r.planning_status.value if r.planning_status else None,
                "date_approved": r.date_approved.isoformat() if r.date_approved else None,
                "date_proposed": r.date_proposed.isoformat() if r.date_proposed else None,
                "date_returned": r.date_returned.isoformat() if r.date_returned else None,
                "date_started": r.date_started.isoformat() if r.date_started else None,
                "date_finished": r.date_finished.isoformat() if r.date_finished else None,
                "operation_status": r.operation_status.value if r.operation_status else None,
                "date_ppp_proposed": r.date_ppp_proposed.isoformat() if r.date_ppp_proposed else None,
                "date_ppp_approved": r.date_ppp_approved.isoformat() if r.date_ppp_approved else None,
                "ppp_status": r.ppp_status.value if r.ppp_status else None,
                "closeout_status": r.closeout_status.value if r.closeout_status else None
            }
            
            data[job_type]['wells'].append(well_data)

        # Convert Counter objects to regular dictionaries
        for job_type in data:
            data[job_type]['planning_status_counts'] = dict(data[job_type]['planning_status_counts'])
            data[job_type]['operation_status_counts'] = dict(data[job_type]['operation_status_counts'])
            data[job_type]['ppp_status_counts'] = dict(data[job_type]['ppp_status_counts'])
            data[job_type]['closeout_status_counts'] = dict(data[job_type]['closeout_status_counts'])

        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}


# # Penggunaan fungsi
# def get_all_data(db: Session):
#     return get_combined_data(db)

# Data Card ATAS PER JOB TYPE
def get_simplified_job_stats_by_type(db: Session, job_type: str) -> Dict:
    # Query untuk mendapatkan statistik
    stats = db.query(
        func.count(Job.id).filter(Job.planning_status != None).label('rencana'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.OPERATING).label('realisasi'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.FINISHED).label('selesai')
    ).filter(Job.job_type == job_type).first()

    return {
        "rencana": stats.rencana,
        "realisasi": stats.realisasi,
        "selesai": stats.selesai
    }


# AMBIL DATA KKS ITUNG PERSENTASE DASHBOARD SKK
def get_kkks_job_data_P(db: Session) -> List[KKKSJobData]:
    job_types = ['exploration', 'development', 'workover', 'wellservice']
    
    query = db.query(
        KKKS.id,
        KKKS.nama_kkks.label('nama_kkks'),
        Job.job_type,
        func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).label('approved_plans'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.OPERATING).label('active_operations'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.FINISHED).label('finished_jobs')
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
                kkks_data[kkks_id][jt] = JobTypeDataP(
                    approved_plans=0,
                    active_operations=0,
                    finished_jobs=0,
                    percentage=0
                )
        
        if job_type in job_types:
            approved_plans = result.approved_plans or 0
            active_operations = result.active_operations or 0
            finished_jobs = result.finished_jobs or 0
            total_operations = active_operations + finished_jobs
            percentage = (total_operations / approved_plans * 100) if approved_plans > 0 else 0
            
            kkks_data[kkks_id][job_type] = JobTypeDataP(
                approved_plans=approved_plans,
                active_operations=active_operations,
                finished_jobs=finished_jobs,
                percentage=round(percentage, 2)
            )
    
    return [KKKSJobData(**data) for data in kkks_data.values()]
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

    # Create aliases for each job type table
    PlanExplorationAlias = aliased(PlanExploration)
    PlanDevelopmentAlias = aliased(PlanDevelopment)
    PlanWorkoverAlias = aliased(PlanWorkover)
    PlanWellServiceAlias = aliased(PlanWellService)

    # Query for planned budget
    planned_budget_query = union_all(
        db.query(
            literal_column("'Exploration'").label('job_type'),
            func.sum(PlanExplorationAlias.total_budget).label('total')
        ).join(Job, Job.job_plan_id == PlanExplorationAlias.id)
        .filter(Job.planning_status == PlanningStatus.APPROVED),

        db.query(
            literal_column("'Development'").label('job_type'),
            func.sum(PlanDevelopmentAlias.total_budget).label('total')
        ).join(Job, Job.job_plan_id == PlanDevelopmentAlias.id)
        .filter(Job.planning_status == PlanningStatus.APPROVED),

        db.query(
            literal_column("'Workover'").label('job_type'),
            func.sum(PlanWorkoverAlias.total_budget).label('total')
        ).join(Job, Job.job_plan_id == PlanWorkoverAlias.id)
        .filter(Job.planning_status == PlanningStatus.APPROVED),

        db.query(
            literal_column("'Well Service'").label('job_type'),
            func.sum(PlanWellServiceAlias.total_budget).label('total')
        ).join(Job, Job.job_plan_id == PlanWellServiceAlias.id)
        .filter(Job.planning_status == PlanningStatus.APPROVED)
    ).alias('planned_budget')

    # Create aliases for each actual job type table
    ActualExplorationAlias = aliased(ActualExploration)
    ActualDevelopmentAlias = aliased(ActualDevelopment)
    ActualWorkoverAlias = aliased(ActualWorkover)
    ActualWellServiceAlias = aliased(ActualWellService)

    # Query for actual budget
    actual_budget_query = union_all(
        db.query(
            literal_column("'Exploration'").label('job_type'),
            func.sum(ActualExplorationAlias.total_budget).label('total')
        ).join(Job, Job.actual_job_id == ActualExplorationAlias.id)
        .filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])),

        db.query(
            literal_column("'Development'").label('job_type'),
            func.sum(ActualDevelopmentAlias.total_budget).label('total')
        ).join(Job, Job.actual_job_id == ActualDevelopmentAlias.id)
        .filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])),

        db.query(
            literal_column("'Workover'").label('job_type'),
            func.sum(ActualWorkoverAlias.total_budget).label('total')
        ).join(Job, Job.actual_job_id == ActualWorkoverAlias.id)
        .filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])),

        db.query(
            literal_column("'Well Service'").label('job_type'),
            func.sum(ActualWellServiceAlias.total_budget).label('total')
        ).join(Job, Job.actual_job_id == ActualWellServiceAlias.id)
        .filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]))
    ).alias('actual_budget')

    # Execute queries
    planned_results = db.execute(db.query(planned_budget_query)).fetchall()
    actual_results = db.execute(db.query(actual_budget_query)).fetchall()

    # Convert query results to dictionaries
    planned_budget = {row.job_type: float(row.total or 0) for row in planned_results}
    actual_budget = {row.job_type: float(row.total or 0) for row in actual_results}

    # Prepare the result
    result = {}
    for job_type in job_types:
        result[job_type] = {
            "planned": planned_budget.get(job_type, 0),
            "actual": actual_budget.get(job_type, 0)
        }

    return result

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
    PlanExplorationAlias = aliased(PlanExploration, name='plan_exploration')
    PlanDevelopmentAlias = aliased(PlanDevelopment, name='plan_development')

    def get_well_status_for_job_type(job_type):
        finished_wells = select(WellInstance.id).distinct().\
            outerjoin(PlanExplorationAlias, PlanExplorationAlias.well_plan_id == WellInstance.id).\
            outerjoin(PlanDevelopmentAlias, PlanDevelopmentAlias.well_plan_id == WellInstance.id).\
            join(Job, or_(
                Job.job_plan_id == PlanExplorationAlias.id,
                Job.job_plan_id == PlanDevelopmentAlias.id
            )).\
            where(Job.operation_status == OperationStatus.FINISHED).\
            where(Job.job_type == job_type)

        well_status_counts = db.query(
            WellInstance.well_status,
            func.count(WellInstance.id).label('count')
        ).filter(WellInstance.id.in_(select(finished_wells.subquery().c.id))).\
         group_by(WellInstance.well_status).all()

        return {status.value: count for status, count in well_status_counts}

    def create_pie_chart(well_status_data, job_type):
        fig = go.Figure(data=[go.Pie(
            labels=list(well_status_data.keys()),
            values=list(well_status_data.values()),
            textinfo='label+percent',
            insidetextorientation='radial'
        )])

        fig.update_layout(
            title_text=f"Well Status Distribution for Finished {job_type} Jobs",
            height=500,
            width=700
        )

        return json.dumps(fig.to_dict(), indent=2)

    exploration_well_status = get_well_status_for_job_type(JobType.EXPLORATION)
    development_well_status = get_well_status_for_job_type(JobType.DEVELOPMENT)

    exploration_chart = create_pie_chart(exploration_well_status, "Exploration")
    development_chart = create_pie_chart(development_well_status, "Development")

    # Combine all well statuses
    all_well_status = {}
    for status, count in exploration_well_status.items():
        all_well_status[status] = all_well_status.get(status, 0) + count
    for status, count in development_well_status.items():
        all_well_status[status] = all_well_status.get(status, 0) + count

    return {
        "exploration": {
            "well_status": exploration_well_status,
            "chart": exploration_chart
        },
        "development": {
            "well_status": development_well_status,
            "chart": development_chart
        },
        "well_status": all_well_status
    }

def calculate_realization_by_kkks_and_job_type(db: Session) -> Dict[str, List[RealizationItem]]:
    results = (
        db.query(
            KKKS.id.label('kkks_id'),
            KKKS.nama_kkks.label('kkks_name'),
            Job.job_type,
            func.count(case((Job.planning_status == PlanningStatus.APPROVED, Job.id))).label('approved_plans'),
            func.count(case((Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), Job.id))).label('completed_operations')
        )
        .join(Job, KKKS.id == Job.kkks_id)
        .group_by(KKKS.id, KKKS.nama_kkks, Job.job_type)
        .all()
    )

    realization_data = {}
    for job_type in JobType:
        realization_data[job_type.value.lower()] = []

    for result in results:
        realization_percentage = (result.completed_operations / result.approved_plans * 100) if result.approved_plans > 0 else 0
        job_type_key = result.job_type.value.lower()
        
        realization_item = RealizationItem(
            kkks_id=result.kkks_id,
            kkks_name=result.kkks_name,
            job_type=job_type_key,
            approved_plans=result.approved_plans,
            completed_operations=result.completed_operations,
            realization_percentage=round(realization_percentage, 2)
        )
        
        realization_data[job_type_key].append(realization_item)
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

def get_kkks_job_counts(db: Session, kkks_id: str) -> Dict[str, int]:
    query = (
        db.query(
            func.count(Job.id).label('total_jobs'),
            func.sum(case((Job.planning_status == PlanningStatus.APPROVED, 1), else_=0)).label('approved_jobs'),
            func.sum(case(
                (Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), 1),
                else_=0
            )).label('realized_jobs'),
            func.sum(case((Job.operation_status == OperationStatus.FINISHED, 1), else_=0)).label('finished_jobs')
        )
        .filter(Job.kkks_id == kkks_id)
    )
    
    result = query.first()
    
    if not result:
        return {
            'total_jobs': 0,
            'approved_jobs': 0,
            'realized_jobs': 0,
            'finished_jobs': 0
        }
    
    job_counts = {
        'total_jobs': result.total_jobs,
        'approved_jobs': result.approved_jobs,
        'realized_jobs': result.realized_jobs,
        'finished_jobs': result.finished_jobs
    }
    
    return job_counts

# Additional helper function to get job data for a specific KKKS
def create_charts(monthly_data: Dict[str, List[TimeSeriesData]], weekly_data: Dict[str, List[TimeSeriesData]], kkks_name: str):
    chart_data = {}
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_year = datetime.now().year

    for job_type in monthly_data.keys():
        monthly = monthly_data[job_type]
        weekly = weekly_data[job_type]

        # Ensure we have data for all months
        all_months = {f"{current_year}-{i+1:02d}": {"planned": 0, "realized": 0} for i in range(12)}
        for item in monthly:
            all_months[item.time_period] = {"planned": item.planned, "realized": item.realized}

        all_weeks = {f"{current_year}-W{i+1:02d}": {"planned": 0, "realized": 0} for i in range(53)}  # Up to 53 weeks
        for item in weekly:
            if item.time_period in all_weeks:
                all_weeks[item.time_period] = {"planned": item.planned, "realized": item.realized}

        week_labels = list(all_weeks.keys())

        job_type_chart = {
            "monthly": {
                "data": [
                    {
                        "type": "bar",
                        "name": f"{job_type.capitalize()} Monthly Planned",
                        "x": months,
                        "y": [all_months[f"{current_year}-{i+1:02d}"]["planned"] for i in range(12)],
                        "marker": {"color": "blue"},
                    },
                    {
                        "type": "bar",
                        "name": f"{job_type.capitalize()} Monthly Realized",
                        "x": months,
                        "y": [all_months[f"{current_year}-{i+1:02d}"]["realized"] for i in range(12)],
                        "marker": {"color": "orange"},
                    },
                ],
                "layout": {
                    "title": f"KKKS: {kkks_name} - {job_type.capitalize()} Monthly Data",
                    "xaxis": {
                        "title": f"{job_type.capitalize()} Month",
                        "tickmode": "array",
                        "tickvals": months,
                        "ticktext": months,
                    },
                    "yaxis": {
                        "title": "Number of Jobs",
                        "range": [0, max(max(item["planned"], item["realized"]) for item in all_months.values()) * 1.1]
                    },
                    "barmode": "group",
                    "bargap": 0.15,
                    "bargroupgap": 0.1
                }
            },
            "weekly": {
                "data": [
                    {
                        "type": "bar",
                        "name": f"{job_type.capitalize()} Weekly Planned",
                        "x": week_labels,
                        "y": [all_weeks[week]["planned"] for week in week_labels],
                        "marker": {"color": "blue"},
                    },
                    {
                        "type": "bar",
                        "name": f"{job_type.capitalize()} Weekly Realized",
                        "x": week_labels,
                        "y": [all_weeks[week]["realized"] for week in week_labels],
                        "marker": {"color": "orange"},
                    },
                ],
                "layout": {
                    "title": f"KKKS: {kkks_name} - {job_type.capitalize()} Weekly Data",
                    "xaxis": {
                        "title": f"{job_type.capitalize()} Week",
                        "tickmode": "array",
                        "tickvals": week_labels[::4],  # Setiap label minggu keempat
                        "ticktext": [f"Week {i+1}" for i in range(0, len(week_labels), 4)],
                        "tickangle": 45,
                    },
                    "yaxis": {
                        "title": "Number of Jobs",
                        "range": [0, max(max(item["planned"], item["realized"]) for item in all_weeks.values()) * 1.1]
                    },
                    "barmode": "group",
                    "bargap": 0.15,
                    "bargroupgap": 0.1
                }
            }
        }

        chart_data[job_type] = job_type_chart

    return chart_data

def get_kkks_job_data(db: Session, kkks_id: str) -> KKKSJobDataChart:
    kkks = db.query(KKKS).filter(KKKS.id == kkks_id).first()
    if not kkks:
        raise HTTPException(status_code=404, detail="KKKS not found")

    job_counts = get_kkks_job_counts(db, kkks_id)
    monthly_data = get_kkks_monthly_data(db, kkks_id)
    weekly_data = get_kkks_weekly_data(db, kkks_id)
    well_job_data = get_well_job_data(db, kkks_id)

    chart_data = create_charts(monthly_data, weekly_data, kkks.nama_kkks)

    # Calculate job type data with null checks
    approved_plans = job_counts.get('approved_jobs', 0) or 0
    realized_jobs = job_counts.get('realized_jobs', 0) or 0
    finished_jobs = job_counts.get('finished_jobs', 0) or 0

    # Avoid division by zero
    percentage = (realized_jobs / approved_plans * 100) if approved_plans > 0 else 0

    job_type_data = JobTypeData(
        approved_plans=approved_plans,
        active_operations=realized_jobs,
        finished_jobs=finished_jobs,
        percentage=round(percentage, 2)
    )

    # Create ChartDataKKKS objects for each job type
    chart_data_kkks = {}
    for job_type, job_chart in chart_data.items():
        monthly_chart = ChartDataKKKS(
            data=[
                ChartDataItem(
                    type=item["type"],
                    name=item["name"],
                    x=item["x"],
                    y=item["y"],
                    marker=item.get("marker")
                )
                for item in job_chart["monthly"]["data"]
            ],
            layout=ChartLayout(
                title=job_chart["monthly"]["layout"]["title"],
                xaxis=ChartAxis(**job_chart["monthly"]["layout"]["xaxis"]),
                yaxis=ChartAxis(**job_chart["monthly"]["layout"]["yaxis"]),
                barmode=job_chart["monthly"]["layout"].get("barmode"),
                bargap=job_chart["monthly"]["layout"].get("bargap"),
                bargroupgap=job_chart["monthly"]["layout"].get("bargroupgap")
            )
        )
        weekly_chart = ChartDataKKKS(
            data=[
                ChartDataItem(
                    type=item["type"],
                    name=item["name"],
                    x=item["x"],
                    y=item["y"],
                    marker=item.get("marker")
                )
                for item in job_chart["weekly"]["data"]
            ],
            layout=ChartLayout(
                title=job_chart["weekly"]["layout"]["title"],
                xaxis=ChartAxis(**job_chart["weekly"]["layout"]["xaxis"]),
                yaxis=ChartAxis(**job_chart["weekly"]["layout"]["yaxis"]),
                barmode=job_chart["weekly"]["layout"].get("barmode"),
                bargap=job_chart["weekly"]["layout"].get("bargap"),
                bargroupgap=job_chart["weekly"]["layout"].get("bargroupgap")
            )
        )
        chart_data_kkks[job_type] = {
            "monthly": monthly_chart,
            "weekly": weekly_chart
        }

    return KKKSJobDataChart(
        id=kkks.id,
        nama_kkks=kkks.nama_kkks,
        job_data=job_type_data,
        monthly_data=monthly_data,
        weekly_data=weekly_data,
        well_job_data=well_job_data,
        chart_data=chart_data_kkks
    )
# Function to get overall dashboard data
def get_dashboard_data(db: Session):
    budget_summary = get_budget_summary_by_job_type(db)
    job_well_status = get_job_and_well_status_summary(db)

    return {
        "budget_summary": budget_summary,
        "job_well_status": job_well_status,
        "exploration_realization": exploration_realization
    }

# Function to get job counts for specific job types and statuses
def generate_rig_type_pie_chart(db: Session) -> Dict:
    # Query to count rig types in PlanDevelopment
    development_counts = db.query(
        PlanDevelopment.rig_type,
        func.count(PlanDevelopment.id).label('count')
    ).group_by(PlanDevelopment.rig_type).all()

    # Query to count rig types in PlanExploration
    exploration_counts = db.query(
        PlanExploration.rig_type,
        func.count(PlanExploration.id).label('count')
    ).group_by(PlanExploration.rig_type).all()

    # Process the results for development
    dev_labels = []
    dev_values = []
    for rig_type, count in development_counts:
        if rig_type is not None:
            dev_labels.append(rig_type.value)
            dev_values.append(count)

    # Process the results for exploration
    exp_labels = []
    exp_values = []
    for rig_type, count in exploration_counts:
        if rig_type is not None:
            exp_labels.append(rig_type.value)
            exp_values.append(count)

    # Create Plotly figures for both charts
    dev_fig = go.Figure(data=[go.Pie(
        labels=dev_labels,
        values=dev_values,
        hole=.3,
        hoverinfo='label+percent+value',
        textinfo='percent',
        insidetextorientation='radial'
    )])

    exp_fig = go.Figure(data=[go.Pie(
        labels=exp_labels,
        values=exp_values,
        hole=.3,
        hoverinfo='label+percent+value',
        textinfo='percent',
        insidetextorientation='radial'
    )])

    # Update layout for both figures
    dev_fig.update_layout(
        title_text="Development Rig Type Distribution",
        height=500,
        width=700
    )

    exp_fig.update_layout(
        title_text="Exploration Rig Type Distribution",
        height=500,
        width=700
    )

    # Convert the figures to JSON
    dev_chart_json = dev_fig.to_json()
    exp_chart_json = exp_fig.to_json()

    # Return the structured data
    return {
        "exploration": {
            "chart_data": exp_chart_json,
            "raw_data": {
                "labels": exp_labels,
                "values": exp_values
            }
        },
        "development": {
            "chart_data": dev_chart_json,
            "raw_data": {
                "labels": dev_labels,
                "values": dev_values
            }
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


def get_all_job_types_data(db: Session) -> Dict[str, Dict]:
    # Query untuk mengambil semua data yang diperlukan
    jobs_data = db.query(
        Job, WellInstance, KKKS, Area, Lapangan, JobInstance,
        func.count(Job.id).over(partition_by=Job.job_type).label('total_jobs'),
        func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).over(partition_by=Job.job_type).label('approved_jobs'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.OPERATING).over(partition_by=Job.job_type).label('operating_jobs'),
        func.count(Job.id).filter(Job.operation_status == OperationStatus.FINISHED).over(partition_by=Job.job_type).label('finished_jobs')
    ).outerjoin(WellInstance, Job.field_id == WellInstance.field_id)\
     .outerjoin(KKKS, Job.kkks_id == KKKS.id)\
     .outerjoin(Area, Job.area_id == Area.id)\
     .outerjoin(Lapangan, Job.field_id == Lapangan.id)\
     .outerjoin(JobInstance, or_(Job.job_plan_id == JobInstance.id, Job.actual_job_id == JobInstance.id))\
     .order_by(Job.job_type, Job.date_proposed).all()

    result = {}
    for job_type in JobType:
        result[job_type.value.lower()] = {
            "summary": {
                "disetujui": 0,
                "beroperasi": 0,
                "selesai": 0
            },
            "job_details": []
        }

    for job, well, kkks, area, field, job_instance, total, approved, operating, finished in jobs_data:
        job_type_key = job.job_type.value.lower()
        
        # Update summary
        result[job_type_key]["summary"]["disetujui"] = approved
        result[job_type_key]["summary"]["beroperasi"] = operating
        result[job_type_key]["summary"]["selesai"] = finished

        # Add job details
        is_plan = job_instance.job_phase_type == 'plan' if job_instance else True
        job_detail = {
            "NO": job.id,
            "NAMA SUMUR": well.well_name if well else "N/A",
            "KKKS": kkks.nama_kkks if kkks else "N/A",
            "WILAYAH KERJA": area.area_name if area else "N/A",
            "LAPANGAN": field.field_name if field else "N/A",
            "RENCANA MULAI": job_instance.start_date.strftime("%d %b %Y") if is_plan and job_instance and job_instance.start_date else "N/A",
            "REALISASI MULAI": job_instance.start_date.strftime("%d %b %Y") if not is_plan and job_instance and job_instance.start_date else "N/A",
            "RENCANA SELESAI": job_instance.end_date.strftime("%d %b %Y") if is_plan and job_instance and job_instance.end_date else "N/A",
            "REALISASI SELESAI": job_instance.end_date.strftime("%d %b %Y") if not is_plan and job_instance and job_instance.end_date else "N/A",
            "STATUS": job.operation_status.value if job.operation_status else job.planning_status.value
        }
        result[job_type_key]["job_details"].append(job_detail)

    return result

def get_p3_data_by_job_type(db: Session) -> Dict[str, Dict]:
    # Query untuk mengambil statistik untuk semua job types
    stats = db.query(
        Job.job_type,
        func.count(Job.id).filter(Job.operation_status == OperationStatus.FINISHED).label('selesai'),
        func.count(Job.id).filter(Job.ppp_status == PPPStatus.PROPOSED).label('diajukan_p3'),
        func.count(Job.id).filter(Job.ppp_status == PPPStatus.APPROVED).label('p3_disetujui')
    ).group_by(Job.job_type).all()

    # Query untuk mengambil detail pekerjaan
    jobs = db.query(Job, WellInstance, KKKS, Area, Lapangan, JobInstance)\
        .filter(or_(Job.operation_status == OperationStatus.FINISHED,
                    Job.ppp_status.in_([PPPStatus.PROPOSED, PPPStatus.APPROVED])))\
        .join(WellInstance, Job.field_id == WellInstance.field_id)\
        .join(KKKS, Job.kkks_id == KKKS.id)\
        .join(Area, Job.area_id == Area.id)\
        .join(Lapangan, Job.field_id == Lapangan.id)\
        .outerjoin(JobInstance, Job.actual_job_id == JobInstance.id)\
        .order_by(Job.job_type, Job.date_ppp_proposed.desc()).all()

    result = {}
    
    # Inisialisasi struktur data untuk setiap job type
    for job_type in JobType:
        result[job_type.value.lower()] = {
            "summary": {
                "selesai": 0,
                "diajukan_p3": 0,
                "p3_disetujui": 0
            },
            "job_details": []
        }

    # Memasukkan data statistik
    for stat in stats:
        job_type_key = stat.job_type.value.lower()
        result[job_type_key]["summary"] = {
            "selesai": stat.selesai,
            "diajukan_p3": stat.diajukan_p3,
            "p3_disetujui": stat.p3_disetujui
        }

    # Memasukkan detail pekerjaan
    for job, well, kkks, area, field, job_instance in jobs:
        job_type_key = job.job_type.value.lower()
        job_detail = {
            "NO": job.id,
            "NAMA SUMUR": well.well_name,
            "KKKS": kkks.nama_kkks,
            "WILAYAH KERJA": area.area_name,
            "LAPANGAN": field.field_name,
            "RENCANA MULAI": job.date_proposed.strftime("%d %b %Y") if job.date_proposed else "N/A",
            "REALISASI MULAI": job.date_started.strftime("%d %b %Y") if job.date_started else "N/A",
            "RENCANA SELESAI": job_instance.end_date.strftime("%d %b %Y") if job_instance and job_instance.end_date else "N/A",
            "REALISASI SELESAI": job.date_finished.strftime("%d %b %Y") if job.date_finished else "N/A",
            "STATUS": get_p3_status(job)
        }
        result[job_type_key]["job_details"].append(job_detail)

    return result

def get_p3_status(job):
    if job.operation_status == OperationStatus.FINISHED:
        if job.ppp_status == PPPStatus.APPROVED:
            return "APPROVED"
        elif job.ppp_status == PPPStatus.PROPOSED:
            return "PROPOSED"
        else:
            return "FINISHED Ops"
    elif job.operation_status == OperationStatus.OPERATING:
        return "OPERATING"
    else:
        return job.planning_status.value if job.planning_status else "N/A"
    
def get_closeout_data_by_job_type(db: Session) -> Dict[str, Dict]:
    # Query untuk mengambil statistik untuk semua job types
    stats = db.query(
        Job.job_type,
        func.count(Job.id).filter(Job.ppp_status == PPPStatus.APPROVED).label('selesai_p3'),
        func.count(Job.id).filter(Job.closeout_status == CloseOutStatus.PROPOSED).label('diajukan_closeout'),
        func.count(Job.id).filter(Job.closeout_status == CloseOutStatus.APPROVED).label('closeout_disetujui')
    ).group_by(Job.job_type).all()

    # Query untuk mengambil detail pekerjaan
    jobs = db.query(Job, WellInstance, KKKS, Area, Lapangan, JobInstance)\
        .filter(or_(Job.ppp_status == PPPStatus.APPROVED,
                    Job.closeout_status.in_([CloseOutStatus.PROPOSED, CloseOutStatus.APPROVED])))\
        .join(WellInstance, Job.field_id == WellInstance.field_id)\
        .join(KKKS, Job.kkks_id == KKKS.id)\
        .join(Area, Job.area_id == Area.id)\
        .join(Lapangan, Job.field_id == Lapangan.id)\
        .outerjoin(JobInstance, Job.actual_job_id == JobInstance.id)\
        .order_by(Job.job_type, Job.date_ppp_approved.desc()).all()

    result = {}
    
    # Inisialisasi struktur data untuk setiap job type
    for job_type in JobType:
        result[job_type.value.lower()] = {
            "summary": {
                "selesai_p3": 0,
                "diajukan_closeout": 0,
                "closeout_disetujui": 0
            },
            "job_details": []
        }

    # Memasukkan data statistik
    for stat in stats:
        job_type_key = stat.job_type.value.lower()
        result[job_type_key]["summary"] = {
            "selesai_p3": stat.selesai_p3,
            "diajukan_closeout": stat.diajukan_closeout,
            "closeout_disetujui": stat.closeout_disetujui
        }

    # Memasukkan detail pekerjaan
    for job, well, kkks, area, field, job_instance in jobs:
        job_type_key = job.job_type.value.lower()
        job_detail = {
            "NO": job.id,
            "NAMA SUMUR": well.well_name,
            "KKKS": kkks.nama_kkks,
            "WILAYAH KERJA": area.area_name,
            "LAPANGAN": field.field_name,
            "RENCANA MULAI": job.date_proposed.strftime("%d %b %Y") if job.date_proposed else "N/A",
            "REALISASI MULAI": job.date_started.strftime("%d %b %Y") if job.date_started else "N/A",
            "RENCANA SELESAI": job_instance.end_date.strftime("%d %b %Y") if job_instance and job_instance.end_date else "N/A",
            "REALISASI SELESAI": job.date_finished.strftime("%d %b %Y") if job.date_finished else "N/A",
            "STATUS": get_closeout_status(job)
        }
        result[job_type_key]["job_details"].append(job_detail)

    return result

def get_closeout_status(job):
    if job.closeout_status == CloseOutStatus.APPROVED:
        return "APPROVED"
    elif job.closeout_status == CloseOutStatus.PROPOSED:
        return "PROPOSED"
    elif job.ppp_status == PPPStatus.APPROVED:
        return "FINISHED P3"
    else:
        return job.operation_status.value if job.operation_status else "N/A"