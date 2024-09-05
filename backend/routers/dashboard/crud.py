from sqlalchemy.orm import Session
from backend.routers.auth.models import *
from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.well.schemas import *
from backend.routers.spatial.schemas import *
from backend.routers.dashboard.schemas import *
from backend.routers.dashboard.models import *
from backend.routers.well.models import *
from typing import Dict
from sqlalchemy import and_,case,or_
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
from datetime import timedelta
from collections import Counter
from sqlalchemy import func, cast, Float
import plotly.graph_objects as go
import calendar
import numpy as np
import pandas as pd
from backend.routers.dashboard.utils import generate_pie_chart, generate_vs_bar_graph, generate_stimulation_graph

job_type_map = {
    'Exploration': JobType.EXPLORATION,
    'Development': JobType.DEVELOPMENT,
    'Workover': JobType.WORKOVER,
    'Well Service': JobType.WELLSERVICE
}

#dashboard per job
def get_plans_dashboard(db: Session, job_type: JobType) -> Dict[str, Dict]:
    
    plans = db.query(Job).filter(Job.job_type == job_type).all()
    result = {}
    
    for i, job in enumerate(plans):

        result = {
            "job_details": [],
            "summary": {
                "disetujui": 0,
                "diusulkan": 0,
                "dikembalikan": 0
            }
        }
        
        job_detail = {
            "id": job.id,
            'NO':i+1,
            "NAMA SUMUR": job.well_name if job.well_name else "N/A",
            "WILAYAH KERJA": job.area_name if job.area_name else "N/A",
            "LAPANGAN": job.field_name if job.field_name else "N/A",
            "KKKS": job.kkks_name if job.kkks_name else "N/A",
            "RENCANA MULAI": job.plan_start_date.strftime("%d %b %Y") if job.plan_start_date else "N/A",
            "RENCANA SELESAI": job.plan_end_date.strftime("%d %b %Y") if job.plan_end_date else "N/A",
            "TANGGAL DIAJUKAN": job.date_proposed.strftime("%d %b %Y") if job.date_proposed else "N/A",
            "STATUS": job.current_status.value
        }
        
        if job.job_type in [JobType.WELLSERVICE, JobType.WORKOVER]:
            job_detail['JENIS PEKERJAAN'] = job.job_plan.job_category.value
        
        result["job_details"].append(job_detail)
        
        # Update summary
        if job.planning_status == PlanningStatus.APPROVED:
            result["summary"]["disetujui"] += 1
        elif job.planning_status == PlanningStatus.PROPOSED:
            result["summary"]["diusulkan"] += 1
        elif job.planning_status == PlanningStatus.RETURNED:
            result["summary"]["dikembalikan"] += 1
    
    return result

def get_operations_dashboard(db: Session, job_type: JobType) -> Dict[str, Dict]:
    
    jobs = db.query(Job).filter(Job.planning_status == PlanningStatus.APPROVED).filter(Job.job_type == job_type).all()
    result = {}
    
    for i, job in enumerate(jobs):

        result = {
            "job_details": [],
            "summary": {
                "disetujui": 0,
                "beroperasi": 0,
                "selesai beroperasi": 0
            }
        }
        
        job_detail = {
            "id": job.id,
            'NO':i+1,
            "NAMA SUMUR": job.well_name if job.well_name else "N/A",
            "WILAYAH KERJA": job.area_name if job.area_name else "N/A",
            "LAPANGAN": job.field_name if job.field_name else "N/A",
            "KKKS": job.kkks_name if job.kkks_name else "N/A",
            "RENCANA MULAI": job.plan_start_date.strftime("%d %b %Y") if job.plan_start_date else "N/A",
            "RENCANA SELESAI": job.plan_end_date.strftime("%d %b %Y") if job.plan_end_date else "N/A",
            "REALISASI MULAI": job.actual_start_date.strftime("%d %b %Y") if job.actual_start_date else "N/A",
            "REALISASI SELESAI": job.actual_end_date.strftime("%d %b %Y") if job.actual_end_date else "N/A",
            "STATUS": job.current_status.value
        }
        
        if job.job_type in [JobType.WELLSERVICE, JobType.WORKOVER]:
            job_detail['JENIS PEKERJAAN'] = job.job_plan.job_category.value
        
        result["job_details"].append(job_detail)
        
        # Update summary
        if job.planning_status == PlanningStatus.APPROVED:
            result["summary"]["disetujui"] += 1
        elif job.planning_status == PlanningStatus.PROPOSED:
            result["summary"]["beroperasi"] += 1
        elif job.planning_status == PlanningStatus.RETURNED:
            result["summary"]["selesai beroperasi"] += 1
    
    return result

def get_ppp_dashboard(db: Session, job_type: JobType) -> Dict[str, Dict]:
    
    jobs = db.query(Job).filter(Job.planning_status == OperationStatus.FINISHED).filter(Job.job_type == job_type).all()
    result = {}
    
    for i, job in enumerate(jobs):

        result = {
            "job_details": [],
            "summary": {
                "selesai beroperasi": 0,
                "diajukan": 0,
                "disetujui": 0
            }
        }
        
        job_detail = {
            "id": job.id,
            'NO':i+1,
            "NAMA SUMUR": job.well_name if job.well_name else "N/A",
            "WILAYAH KERJA": job.area_name if job.area_name else "N/A",
            "LAPANGAN": job.field_name if job.field_name else "N/A",
            "KKKS": job.kkks_name if job.kkks_name else "N/A",
            "REALISASI MULAI": job.actual_start_date.strftime("%d %b %Y") if job.actual_start_date else "N/A",
            "REALISASI SELESAI": job.actual_end_date.strftime("%d %b %Y") if job.actual_end_date else "N/A",
            "TANGGAL P3 DIAJUKAN": job.date_ppp_proposed.strftime("%d %b %Y") if job.date_ppp_proposed else "N/A",
            "TANGGAL P3 DISETUJUI": job.date_ppp_approved.strftime("%d %b %Y") if job.date_ppp_approved else "N/A",
            "STATUS": job.current_status.value
        }
        
        if job.job_type in [JobType.WELLSERVICE, JobType.WORKOVER]:
            job_detail['JENIS PEKERJAAN'] = job.job_plan.job_category.value
        
        result["job_details"].append(job_detail)
        
        # Update summary
        if job.planning_status == PlanningStatus.APPROVED:
            result["summary"]["selesai beroperasi"] += 1
        elif job.planning_status == PlanningStatus.PROPOSED:
            result["summary"]["diajukan"] += 1
        elif job.planning_status == PlanningStatus.RETURNED:
            result["summary"]["disetujui"] += 1
    
    return result

def get_co_dashboard(db: Session, job_type: JobType) -> Dict[str, Dict]:
    
    jobs = db.query(Job).filter(Job.planning_status == PPPStatus.APPROVED).filter(Job.job_type == job_type).all()
    result = {}
    
    for i, job in enumerate(jobs):

        result = {
            "job_details": [],
            "summary": {
                "selesai p3": 0,
                "diajukan": 0,
                "disetujui": 0
            }
        }
        
        job_detail = {
            "id": job.id,
            'NO':i+1,
            "NAMA SUMUR": job.well_name if job.well_name else "N/A",
            "WILAYAH KERJA": job.area_name if job.area_name else "N/A",
            "LAPANGAN": job.field_name if job.field_name else "N/A",
            "KKKS": job.kkks_name if job.kkks_name else "N/A",
            "REALISASI MULAI": job.actual_start_date.strftime("%d %b %Y") if job.actual_start_date else "N/A",
            "REALISASI SELESAI": job.actual_end_date.strftime("%d %b %Y") if job.actual_end_date else "N/A",
            "TANGGAL CO DIAJUKAN": job.date_co_proposed.strftime("%d %b %Y") if job.date_co_proposed else "N/A",
            "TANGGAL CO DISETUJUI": job.date_co_approved.strftime("%d %b %Y") if job.date_co_approved else "N/A",
            "STATUS": job.current_status.value
        }
        
        if job.job_type in [JobType.WELLSERVICE, JobType.WORKOVER]:
            job_detail['JENIS PEKERJAAN'] = job.job_plan.job_category.value
        
        result["job_details"].append(job_detail)
        
        # Update summary
        if job.planning_status == PlanningStatus.APPROVED:
            result["summary"]["selesai p3"] += 1
        elif job.planning_status == PlanningStatus.PROPOSED:
            result["summary"]["diajukan"] += 1
        elif job.planning_status == PlanningStatus.RETURNED:
            result["summary"]["disetujui"] += 1
    
    return result

#home dashboard
def get_dashboard_progress_tablechart(db: Session) -> Dict:

    results = db.query(
        Job.job_type,
        func.count(Job.id).filter(Job.planning_status == PlanningStatus.APPROVED).label('rencana'),
        func.count(Job.id).filter(Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED])).label('realisasi'),
        func.count(Job.id).filter(Job.actual_start_date == datetime.now().date()).label('change'),
    ).group_by(Job.job_type).all()

    dashboard_table_data = {}
    
    for result in results:
        job_type = result.job_type.value.lower()
        dashboard_table_data[job_type] = {}
        dashboard_table_data[job_type]["rencana"] = result.rencana
        dashboard_table_data[job_type]["realisasi"] = result.realisasi
    
    job_types = list(job_type_map.keys())
    
    fig = go.Figure(data=[
        go.Bar(name='Rencana', x=job_types, y=[dashboard_table_data[job_type_map[job_type].value.lower()]["rencana"] for job_type in job_types]),
        go.Bar(name='Realisasi', x=job_types, y=[dashboard_table_data[job_type_map[job_type].value.lower()]["realisasi"] for job_type in job_types])
    ])

    fig.update_layout(barmode='group')
    fig.update_layout(template='plotly_white')
    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)
    
    return {
        'table':dashboard_table_data,
        'plot':fig_data
    }

def get_dashboard_kkks_table(db: Session) -> Dict:
    
    columns = [
        KKKS.id,
        KKKS.name.label('name')
        ] + [
        (cast(func.count(Job.id).filter(
            and_(
                or_(
                    Job.operation_status == OperationStatus.OPERATING,
                    Job.operation_status == OperationStatus.FINISHED,
                ),
                Job.job_type == job_type
            )
        ), Float) / 
        cast(func.count(Job.id).filter(
            and_(
                Job.planning_status == PlanningStatus.APPROVED,
                Job.job_type == job_type
            )
        ), Float) * 100).label(f'{job_type.value.lower().replace(" ", "")}_percentage') for job_type in JobType ]

    query = db.query(
        *columns
        ).outerjoin(Job, KKKS.id == Job.kkks_id).group_by(KKKS.id, KKKS.name)

    results = query.all()

    kkks_data = []
    for result in results:

        kkks_data.append(
            dict(
                id=result.id,
                name=result.name,
                exploration_percentage=f'{round(result.exploration_percentage, 2)}%' if result.exploration_percentage else 0,
                development_percentage=f'{round(result.development_percentage, 2)}%' if result.development_percentage else 0,
                workover_percentage=f'{round(result.workover_percentage, 2)}%' if result.workover_percentage else 0,
                wellservice_percentage=f'{round(result.wellservice_percentage, 2)}%' if result.wellservice_percentage else 0,
            )  
        )

    return kkks_data

#make graph
def make_job_graph(db: Session, job_type: JobType, periods: list) -> Dict[str, Dict]:
    
    current_year = datetime.now().year ##todo: sync with wpnb year

    # Query for planned jobs
    rencana = db.query(
        (Job.plan_start_date).label('plan_start_date'),
    ).filter(
        Job.job_type == job_type,
        Job.planning_status == PlanningStatus.APPROVED,
        Job.wpb_year == current_year).all()

    # Query for realized jobs
    realisasi = db.query(
        (Job.actual_start_date).label('actual_start_date'),
    ).filter(
        Job.job_type == job_type,
        Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]),
        Job.wpb_year == current_year).all()
    
    list_rencana = [date.plan_start_date for date in rencana]
    list_realisasi = [date.actual_start_date for date in realisasi]
    
    output = {}
    
    if 'month' in periods:
        
        months_rencana = [date.strftime("%B") if date is not None else None for date in list_rencana]
        months_realisasi = [date.strftime("%B") if date is not None else None for date in list_realisasi]

        m=[]
        j_rencana=[]
        j_realisasi=[]

        month_counts_rencana = Counter(months_rencana)
        month_counts_realisasi = Counter(months_realisasi)
        month_names = calendar.month_name[1:]

        for month in month_names:
            m.append(f'{month} {current_year}')
            j_rencana.append(month_counts_rencana.get(month, 0))
            j_realisasi.append(month_counts_realisasi.get(month, 0))

        rencanasum = np.cumsum(j_rencana)
        realisasisum = np.cumsum(j_realisasi)

        # Graph components
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(y=j_rencana, x=m, name="Rencana", marker_color="#eb2427"),secondary_y=False)
        fig.add_trace(go.Bar(y=j_realisasi, x=m, name="Realisasi", marker_color="#bcd42c"),secondary_y=False)
        fig.add_trace(go.Scatter(y=rencanasum, x=m, name="Outlook Kumulatif", marker_color="#eb2427"),secondary_y=True)
        fig.add_trace(go.Scatter(y=realisasisum, x=m, name="Realisasi Kumulatif", marker_color="#bcd42c"),secondary_y=True)
        fig.update_layout(hovermode='x unified')
        fig.update_layout(template='plotly_white')
        fig['layout']['margin'] = {'l': 10, 'r': 10, 'b': 10, 't': 10}
        fig['layout']['xaxis']['type'] = 'category'
        fig['layout']['yaxis2']['showgrid'] = False
        
        fig_json = fig.to_json(pretty=True, engine="json")
        fig_data = json.loads(fig_json)
        
        output['month'] = fig_data
    
    if 'week' in periods:
        
        def get_week(date):
            week_num = (date.day - 1) // 7 + 1
            return f'M{week_num} {date.strftime("%B %Y")}'
        
        rencana = pd.to_datetime(pd.Series(list_rencana)).apply(get_week)
        ralisasi = pd.to_datetime(pd.Series(list_realisasi)).apply(get_week)
        
        current_year = 2024

        start_date = datetime(current_year, 1, 1).date()
        end_date = datetime(current_year, 12, 31).date()

        week_list = []
        current_date = start_date
        while current_date <= end_date:
            week_number = (current_date.day - 1) // 7 + 1
            label = f"M{week_number} {current_date.strftime('%B')} {current_date.year}"
            week_list.append(label)
            current_date += timedelta(days=7)
        
        w=week_list
        j_rencana=[]
        j_realisasi=[]

        week_counts_rencana = Counter(rencana)
        week_counts_realisasi = Counter(ralisasi)
        
        for week in week_list:
            try:
                j_rencana.append(week_counts_rencana[week])
            except:
                j_rencana.append(0)
            try:
                j_realisasi.append(week_counts_realisasi[week])
            except:
                j_realisasi.append(0)

        rencanasum = np.cumsum(j_rencana)
        realisasisum = np.cumsum(j_realisasi)

        # Graph components
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(y=j_rencana, x=w, name="Rencana", marker_color="#eb2427"),secondary_y=False)
        fig.add_trace(go.Bar(y=j_realisasi, x=w, name="Realisasi", marker_color="#bcd42c"),secondary_y=False)
        fig.add_trace(go.Scatter(y=rencanasum, x=w, name="Outlook Kumulatif", marker_color="#eb2427"),secondary_y=True)
        fig.add_trace(go.Scatter(y=realisasisum, x=w, name="Realisasi Kumulatif", marker_color="#bcd42c"),secondary_y=True)
        fig.update_layout(hovermode='x unified')
        fig.update_layout(template='plotly_white')
        fig['layout']['xaxis']['type'] = 'category'
        fig['layout']['margin'] = {'l': 10, 'r': 10, 'b': 10, 't': 10}
        fig['layout']['yaxis2']['showgrid'] = False
        
        fig_json = fig.to_json(pretty=True, engine="json")
        fig_data = json.loads(fig_json)
        
        output['week'] = fig_data

    return output

def get_job_type_summary(db: Session, job_type: JobType):
   
    result = db.query(
        func.count(
            case(
                (Job.planning_status == PlanningStatus.APPROVED, 1),
                else_=None
            )
        ).label('rencana'),
        func.count(
            case(
                (Job.operation_status.in_([OperationStatus.OPERATING, OperationStatus.FINISHED]), 1),
                else_=None
            )
        ).label('realisasi'),
        func.count(
            case(
                (Job.operation_status == OperationStatus.FINISHED, 1),
                else_=None
            )
        ).label('selesai')
    ).filter(Job.job_type == job_type).first()

    return {
        'rencana': result.rencana,
        'realisasi': result.realisasi,
        'selesai': result.selesai
    }

def get_kkks_table_by_job_type(db: Session, job_type: JobType):
    
    columns = [
        KKKS.id,
        KKKS.name.label('name'),
        (func.count(Job.id).filter(
            Job.planning_status == PlanningStatus.APPROVED,
            Job.job_type == job_type,
        )).label('rencana'),
        (func.count(Job.id).filter(
            and_(
                or_(
                    Job.operation_status == OperationStatus.OPERATING,
                    Job.operation_status == OperationStatus.FINISHED,
                ),
                Job.job_type == job_type
            )
        )).label('realisasi'),
    ]

    query = db.query(
        *columns
        ).outerjoin(Job, KKKS.id == Job.kkks_id).group_by(KKKS.id, KKKS.name)

    results = query.all()

    kkks_data = []
    for result in results:

        kkks_data.append(
            dict(
                id=result.id,
                name=result.name,
                rencana=result.rencana,
                realisasi=result.realisasi,
                percentage=f'{round(result.rencana / result.realisasi * 100, 2)}%' if result.realisasi > 0 else 0,
            )  
        )

    return kkks_data

def get_costs_by_job_type(db: Session, job_type: JobType):
    
    query = db.query(
        func.sum(Job.plan_total_budget).filter(
            Job.job_type == job_type,
            Job.planning_status == PlanningStatus.APPROVED,
        ).label('rencana'),
        func.sum(Job.actual_total_budget).filter(
            and_(
                or_(
                    Job.operation_status == OperationStatus.OPERATING,
                    Job.operation_status == OperationStatus.FINISHED,
                ),
                Job.job_type == job_type
            )
        ).label('realisasi'),
    )
    
    result = query.first()
    
    return {
        'rencana': result.rencana,
        'realisasi': result.realisasi,
    }

def get_actual_well_status_by_job_type(db: Session, job_type: JobType):

    result = (
        db.query(WellInstance.well_status.label('well_status'), func.count(WellInstance.well_status).label('count'))
        .join(JobInstance, JobInstance.well_id == WellInstance.well_instance_id)
        .join(Job, Job.job_plan_id == JobInstance.job_instance_id)
        .filter(Job.job_type == job_type, 
            or_(
                Job.operation_status == OperationStatus.OPERATING,
                Job.operation_status == OperationStatus.FINISHED
            ))
        .group_by(ActualWell.well_status)
        .all()
    )
    
    if result:
        output = {}
        for row in result:
            output[row.well_status.value] = row.count
        return output
    else:
        return None

def get_well_stimulation_by_job_type(db: Session, job_type: JobType):
    
    if job_type == JobType.WORKOVER:
        plan_job_model = PlanWorkover
        actual_job_model = ActualWorkover
    elif job_type == JobType.WELLSERVICE:
        plan_job_model = PlanWellService
        actual_job_model = ActualWellService
    
    result_current = (
        db.query(
            func.sum(plan_job_model.onstream_oil).label('current_onstream_oil'), 
            func.sum(plan_job_model.onstream_gas).label('current_onstream_gas'), 
            )
        .join(Job, Job.job_plan_id == plan_job_model.job_instance_id)
        .filter(Job.job_type == job_type, 
            Job.planning_status == PlanningStatus.APPROVED)
        .first()
    )
    
    result_final = (
        db.query(
            func.sum(actual_job_model.onstream_oil).label('final_onstream_oil'), 
            func.sum(actual_job_model.onstream_gas).label('final_onstream_gas'), 
        )
        .join(Job, Job.job_plan_id == actual_job_model.job_instance_id)
        .filter(Job.job_type == job_type, 
            or_(
                Job.operation_status == OperationStatus.OPERATING,
                Job.operation_status == OperationStatus.FINISHED
            ))
        .first()
    )

    output = {
        'current_onstream_oil': result_current.current_onstream_oil,
        'current_onstream_gas': result_current.current_onstream_gas,
        'final_onstream_oil': result_final.final_onstream_oil,
        'final_onstream_gas': result_final.final_onstream_gas,
    }

    return output

def get_environment_type_by_job_type(db: Session, job_type: JobType):
    
    result = (
        db.query(WellInstance.environment_type.label('environment_type'), func.count(WellInstance.environment_type).label('count'))
        .join(JobInstance, JobInstance.well_id == WellInstance.well_instance_id)
        .join(Job, Job.job_plan_id == JobInstance.job_instance_id)
        .filter(Job.job_type == job_type, 
            or_(
                Job.operation_status == OperationStatus.OPERATING,
                Job.operation_status == OperationStatus.FINISHED
            ))
        .group_by(ActualWell.environment_type)
        .all()
    )
    
    if result:
        output = {}
        for row in result:
            output[row.environment_type.value] = row.count
        return output
    else:
        return None

def get_job_type_dashboard(db: Session, job_type: JobType):
    
    cost = get_costs_by_job_type(db, job_type)
    cost_graph = generate_vs_bar_graph([cost['rencana'], cost['realisasi']], ['Plan Cost', 'Actual Cost'], orientation='h')

    output = {
        'summary': get_job_type_summary(db, job_type),
        'job_graph': make_job_graph(db, job_type, ['month']),
        'cost_graph': cost_graph,
    }
    
    if job_type in [JobType.WELLSERVICE, JobType.WORKOVER]:
        well_stimulation = get_well_stimulation_by_job_type(db, job_type)
        well_stimulation_graph = generate_stimulation_graph(well_stimulation)
        output['well_stimulation_graph'] = well_stimulation_graph
    else:
        status_akhir = get_actual_well_status_by_job_type(db, job_type)
        status_akhir_graph = generate_pie_chart(list(status_akhir.values()), list(status_akhir.keys()))
        environment_type = get_environment_type_by_job_type(db, job_type)
        environment_type_graph = generate_pie_chart(list(environment_type.values()), list(environment_type.keys()))
        output['status_akhir_graph'] = status_akhir_graph
        output['environment_type_graph'] = environment_type_graph
    
    return output