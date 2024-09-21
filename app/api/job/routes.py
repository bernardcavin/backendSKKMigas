from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_db, get_current_user
from app.api.job import crud, schemas
from app.api.job.models import JobType,Job
from app.core.schema_operations import create_api_response
from typing import Any

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/planning/create/exploration")
@authorize(role=[Role.KKKS])
async def create_planning_exploration(plan: schemas.CreateExplorationJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.EXPLORATION, plan, user)
    return create_api_response(success=True, message="Exploration job plan created successfully", data={"id": job_id})

@router.post("/planning/create/development")
@authorize(role=[Role.KKKS])
async def create_planning_development(plan: schemas.CreateDevelopmentJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.DEVELOPMENT, plan, user)
    return create_api_response(success=True, message="Development job plan created successfully", data={"id": job_id})

@router.post("/planning/create/workover")
@authorize(role=[Role.KKKS])
async def create_planning_workover(plan: schemas.CreateWorkoverJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WORKOVER, plan, user)
    return create_api_response(success=True, message="Workover job plan created successfully", data={"id": job_id})

@router.post("/planning/create/wellservice")
@authorize(role=[Role.KKKS])
async def create_planning_wellservice(plan: schemas.CreateWellServiceJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WELLSERVICE, plan, user)
    return create_api_response(success=True, message="Well service job plan created successfully", data={"id": job_id})

@router.delete('/planning/delete/{job_id}')
@authorize(role=[Role.Admin, Role.KKKS])
async def delete_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    deleted = crud.delete_job_plan(job_id, db, user)
    if not deleted:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan deleted successfully")

@router.patch('/planning/approve/{job_id}')
@authorize(role=[Role.Admin])
async def approve_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    approved = crud.approve_job_plan(job_id, db, user)
    if not approved:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan approved successfully")

@router.patch('/planning/return/{job_id}')
@authorize(role=[Role.Admin])
async def return_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    returned = crud.return_job_plan(job_id, db, user)
    if not returned:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan returned successfully")

@router.get('/planning/view/{job_id}')
@authorize(role=[Role.Admin, Role.KKKS])
async def view_plan(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_plan = crud.get_job_plan(job_id, db)
    if not job_plan:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan retrieved successfully", data=job_plan)

@router.patch('/operations/operate/{job_id}')
@authorize(role=[Role.Admin, Role.KKKS])
async def operate_job(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    operated = crud.operate_job(job_id, db, user)
    if not operated:
        return create_api_response(success=False, message="Job not found or operation failed", status_code=404)
    return create_api_response(success=True, message="Job operation started successfully")

# @router.get("/jobs/{job_id}", response_model=schemas.JobDetail)
# def get_job_detail(job_id: str, db: Session = Depends(get_db)):
#     job = db.query(Job).filter(Job.id == job_id).first()
#     if not job:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return job


@router.post("/daily-operations-reports/")
def create_daily_operations_report(report: schemas.DailyOperationsReportCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == report.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.create_daily_operations_report(db=db, report=report)

@router.patch("/actual-exploration/{actual_exploration_id}", response_model=schemas.ActualExplorationUpdate)
def update_actual_exploration(
    exploration_id: str,
    exploration_update: schemas.ActualExplorationUpdate,
    db: Session = Depends(get_db)) -> Any:
    updated_exploration = crud.update_actual_exploration(db, exploration_id, exploration_update)
    if not updated_exploration:
        raise HTTPException(status_code=404, detail="Actual Exploration not found")
    return updated_exploration

@router.post("/create-job-issues/", response_model=schemas.JobIssueResponse)
def create_job_issue(
    job_issue: schemas.JobIssueCreate,
    db: Session = Depends(get_db)
) -> Any:
    return crud.create_job_issue(db=db, job_issue=job_issue)

@router.patch("/job-issues/{job_issue_id}", response_model=schemas.JobIssueResponse)
def update_job_issue(
    job_issue_id: str,
    job_issue_update: schemas.JobIssueUpdate,
    db: Session = Depends(get_db)
) -> Any:
    updated_job_issue = crud.update_job_issue(db=db, job_issue_id=job_issue_id, job_issue_update=job_issue_update)
    if updated_job_issue is None:
        raise HTTPException(status_code=404, detail="Job issue not found")
    return updated_job_issue

@router.get("/jobs/{job_id}/wrm", response_model=schemas.ActualExplorationUpdate)
def get_wrm_data(
    job_id: str,
    db: Session = Depends(get_db)
) -> Any:
    wrm_data = crud.get_wrm_data_by_job_id(db=db, job_id=job_id)
    if wrm_data is None:
        raise HTTPException(status_code=404, detail="WRM data not found for this job")
    return wrm_data

@router.get("/jobs/{job_id}/wrmissues", response_model=schemas.JobIssueCreate)
def get_wrmissues_data(
    job_id: str,
    db: Session = Depends(get_db)
) -> Any:
    wrmissues_data = crud.get_wrmissues_data_by_job_id(db=db, job_id=job_id)
    if wrmissues_data is None:
        raise HTTPException(status_code=404, detail="WRM data not found for this job")
    return wrmissues_data


