from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from backend.routers.job.models import *
from backend.routers.well.schemas import *
from backend.routers.well.models import *
from backend.routers.spatial.models import *
from backend.routers.dashboard.crud import *


from backend.routers.auth.utils import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

job_type_map = {
    'exploration':JobType.EXPLORATION,
    'development':JobType.DEVELOPMENT,
    'workover':JobType.WORKOVER,
    'wellservice':JobType.WELLSERVICE
}

job_phase_map = {
    'plan': get_plans_dashboard,
    'operation': get_operations_dashboard,
    'ppp': get_ppp_dashboard,
    'co': get_co_dashboard,
}

@router.get("/job-phase/{job_type}/{job_phase}")
async def get_job_dashboard(job_type: str, job_phase: str, db: Session = Depends(get_db)):
    return job_phase_map[job_phase](db, job_type_map[job_type])

@router.get("/home", response_model=Dict)
async def get_home_dashboard(db: Session = Depends(get_db)):
    return {
        'tablechart': get_dashboard_progress_tablechart(db),
        'tablekkks': get_dashboard_kkks_table(db)
    }

@router.get("/view-job/{job_type}/")
async def view_job_progress(job_type: str, db: Session = Depends(get_db)):
    return make_job_graph(db, job_type_map[job_type], ['month','week'])

@router.get("/job/{job_type}")
async def test(job_type: str, db: Session = Depends(get_db)):
    return get_job_type_dashboard(db, job_type_map[job_type])




# @router.get("/kkks-job-data", response_model=List[KKKSJobDataCombined])
# def read_kkks_job_data(db: Session = Depends(get_db)):
#     return get_kkks_job_data_P(db)

# @router.get("/aggregate-job-data", response_model=AggregateJobData)
# def read_aggregate_job_data(db: Session = Depends(get_db)):
#     try:
#         aggregate_data = get_aggregate_job_data(db)
#         changes = get_job_data_change(db)

#         result = {}
#         for job_type in ['exploration', 'development', 'workover', 'wellservice']:
#             data = aggregate_data.get(job_type, {'plan': 0, 'realization': 0})
#             change = changes.get(job_type, 0)

#             plan = data.get('plan', 0)
#             realization = data.get('realization', 0)
#             total = plan + realization
            
#             # Calculate percentage
#             percentage = (realization / plan * 100) if plan > 0 else 0
#             percentage = round(percentage, 2)  # Round to 2 decimal places

#             result[job_type] = JobTypeDataUP(
#                 total=total,
#                 plan=plan,
#                 realization=realization,
#                 percentage=percentage,
#                 change=change
#             )

#         return AggregateJobData(**result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# @router.get("/job-summary-chart", response_model=Dict)
# async def get_job_summary_chart(db: Session = Depends(get_db)):
#     """
#     Endpoint to get job summary chart data for Plotly visualization.
#     """
#     chart_data = generate_job_summary_chart_data_json(db)
#     return chart_data

# @router.get("/job-type-summary-skk", response_model=JobTypeSummaryResponse)
# async def read_job_type_summary(db: Session = Depends(get_db)):
#     summary_dict = get_job_type_summary(db)
#     job_type_summary = JobTypeSummaryCard(
#         job_type=summary_dict,
#         rencana=summary_dict,  # Anda mungkin perlu menyesuaikan ini
#         realisasi=summary_dict,  # Anda mungkin perlu menyesuaikan ini
#         selesai=summary_dict  # Anda mungkin perlu menyesuaikan ini
#     )
#     return JobTypeSummaryResponse(job_type_summary=job_type_summary)


# # REALIASI KEGIATAN CHART DASHBOARD SKK
# @router.get("/job-charts", response_model=Dict)
# async def get_job_charts(db: Session = Depends(get_db)):
#     return generate_job_chart_data(db)

# @router.get("/budget-summary-charts", response_model=BudgetSummaryResponse)
# async def read_budget_summary_charts(db: Session = Depends(get_db)):
#     budget_data = get_budget_summary_by_job_type(db)
    
#     charts = {}
#     for job_type, data in budget_data.items():
#         charts[job_type] = ChartData(
#             data=[{
#                 "y": ["Plan", "Actual"],
#                 "x": [data["planned"], data["actual"]],
#                 "type": "bar",
#                 "orientation": "h",
#                 "marker": {
#                     "color": ["rgba(103, 58, 183, 0.8)", "rgba(156, 39, 176, 0.8)"]
#                 }
#             }],
#             layout={
#                 "title": f"{job_type.capitalize()} Budget",
#                 "xaxis": {"title": "Budget (million US$)"},
#                 "height": 400,
#                 "width": 500,
#                 "margin": {"l": 100}  # Increase left margin for labels
#             }
#         )
    
#     return BudgetSummaryResponse(charts=charts)

# @router.get("/job-well-status-summary", response_model=JobAndWellStatusSummary)
# async def read_job_and_well_status_summary(db: Session = Depends(get_db)):
#     """
#     Get a summary of job and well status for Exploration and Development.
    
#     Returns:
#     - Exploration job counts and Plotly chart
#     - Development job counts and Plotly chart
#     - Overall well status distribution
#     """
#     return get_job_and_well_status_summary(db)


# @router.get("/exploration-realization", response_model=Dict[str, List[RealizationItem]])
# def read_exploration_realization(db: Session = Depends(get_db)):
#     return calculate_realization_by_kkks_and_job_type(db)

# # DETAIL KKS 
# @router.get("/kkks/{kkks_id}/job-data", response_model=KKKSJobDataChart)
# def read_kkks_job_data(kkks_id: str, db: Session = Depends(get_db)):
#     return get_kkks_job_data(db, kkks_id)

# @router.get("/job-counts/planning", response_model=List[JobCountResponse])
# def job_counts(db: Session = Depends(get_db)):
#     try:
#         # Default job_types dan statuses
#         job_type = ["exploration", "development", "workover","wellservices"]  # Sesuaikan dengan tipe pekerjaan yang ada di database
#         statuses = ["Proposed", "Approved", "Returned"]  # Sesuaikan dengan status yang ada di database

#         # Query untuk menghitung jumlah berdasarkan job_type dan status
#         query = (
#             db.query(
#                 Job.job_type,
#                 JobInstance.status,
#                 func.count().label('count')
#             )
#             .join(JobInstance, Job.id == JobInstance.proposed_job_id)
#             .group_by(Job.job_type, JobInstance.status)
#         )
#         print(query)
        
#         results = query.all()
#         print(results)

#         if not results:
#             raise HTTPException(status_code=404, detail="No data found")

#         job_counts = [
#             JobCountResponse(
#                 job_type=job_type or "Unknown",
#                 status=status or "Unknown",
#                 count=count or 0
#             )
#             for job_type, status, count in results
#         ]

#         return job_counts

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/rig-type-pie-chart", response_model=Dict)
# async def read_rig_type_pie_chart(db: Session = Depends(get_db)):
#     """
#     Get rig type distribution pie chart data.
#     """
#     return generate_rig_type_pie_chart(db)

# @router.get("/jobs/typedetail", response_model=JobTypeGroup)
# async def read_jobs_grouped(db: Session = Depends(get_db)):
#     jobs = get_jobs(db)
#     return JobTypeGroup(root=jobs)

# @router.get("/all-job-stats")
# async def read_all_job_stats(db: Session = Depends(get_db)):
#     try:
#         all_stats = {}
#         for job_type in JobType:
#             all_stats[job_type.value] = get_simplified_job_stats_by_type(db, job_type)
#         return all_stats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

# @router.get("/data-operations")
# async def read_exploration_operations(db: Session = Depends(get_db)):
#     return get_all_job_types_data(db)    

# @router.get("/data-p3")
# async def read_p3_exploration(db: Session = Depends(get_db)):
#     return get_job_details(db)

# @router.get("/data-closeout")
# async def read_closeout_data(db: Session = Depends(get_db)):
#     return get_closeout_data_by_job_type(db)