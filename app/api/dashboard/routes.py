from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from app.api.auth.crud import get_kkks
from app.api.dashboard.crud import (
    get_plans_dashboard,
    get_operations_dashboard,
    get_ppp_dashboard,
    get_co_dashboard,
    get_dashboard_progress_tablechart,
    get_dashboard_kkks_table,
    make_job_graph,
    get_job_type_dashboard,
    get_kkks_info
)
from app.core.security import authorize, get_current_user, get_db
from app.api.auth.models import Role, Admin, KKKS
from app.api.job.models import JobType
from app.core.schema_operations import create_api_response

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

job_type_map = {
    'exploration': JobType.EXPLORATION,
    'development': JobType.DEVELOPMENT,
    'workover': JobType.WORKOVER,
    'wellservice': JobType.WELLSERVICE
}

job_phase_map = {
    'plan': get_plans_dashboard,
    'operation': get_operations_dashboard,
    'ppp': get_ppp_dashboard,
    'co': get_co_dashboard,
}

@router.get("/job-phase/{job_type}/{job_phase}")
@authorize(role=[Role.Admin, Role.KKKS])
async def get_job_dashboard(job_type: str, job_phase: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if job_phase not in job_phase_map or job_type not in job_type_map:
        return create_api_response(success=False, message="Invalid job type or phase", status_code=400)
    result = job_phase_map[job_phase](db, job_type_map[job_type], user)
    return create_api_response(success=True, message="Dashboard data retrieved successfully", data=result)

@router.get("/home")
@authorize(role=[Role.Admin, Role.KKKS])
async def get_home_dashboard(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if isinstance(user, Admin):
        result = {
            'tablechart': get_dashboard_progress_tablechart(db, user),
            'tablekkks': get_dashboard_kkks_table(db)
        }
    else:
        result = {
            'tablechart': get_dashboard_progress_tablechart(db, user),
        }

    return create_api_response(success=True, message="Home dashboard data retrieved successfully", data=result)

@router.get("/view-job/{job_type}/")
@authorize(role=[Role.Admin, Role.KKKS])
async def view_job_progress(job_type: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if job_type not in job_type_map:
        return create_api_response(success=False, message="Invalid job type", status_code=400)
    result = make_job_graph(db, job_type_map[job_type], ['month', 'week'], user)
    return create_api_response(success=True, message="Job progress data retrieved successfully", data=result)

@router.get("/job/{job_type}")
@authorize(role=[Role.Admin, Role.KKKS])
async def get_job_type_dashboard_endpoint(job_type: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if job_type not in job_type_map:
        return create_api_response(success=False, message="Invalid job type", status_code=400)
    result = get_job_type_dashboard(db, job_type_map[job_type], user)
    return create_api_response(success=True, message="Job type dashboard data retrieved successfully", data=result)

@router.get("/view-kkks/{kkks_id}")
@authorize(role=[Role.Admin, Role.KKKS])
async def view_kkks(kkks_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    kkks = db.query(KKKS).filter(KKKS.id == kkks_id).first()
    if kkks is None:
        raise HTTPException(status_code=404, detail="KKKS not found")
    result = get_kkks_info(db, kkks_id, user)
    return create_api_response(success=True, message="KKKS info retrieved successfully", data=result)
