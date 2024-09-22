from calendar import c
from fastapi import APIRouter, Depends,status,HTTPException, UploadFile, File,Query
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_db, get_current_user
from app.api.job import crud, schemas,models
from app.api.job.models import JobType,Job
from app.core.schema_operations import create_api_response
from typing import Any, Union, List
from datetime import datetime, timedelta

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/planning/upload-batch/exploration")
async def upload_batch_exploration(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch_exploration(db, content, JobType.EXPLORATION, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/development")
async def upload_batch_development(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch_exploration(db, content, JobType.DEVELOPMENT, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/workover")
async def upload_batch_workover(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch_exploration(db, content, JobType.WORKOVER, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/wellservice")
async def upload_batch_wellservice(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch_exploration(db, content, JobType.WELLSERVICE, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/create/exploration")
@authorize(role=[Role.KKKS])
async def create_planning_exploration(plan: schemas.CreateExplorationJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.EXPLORATION, plan, user)
    return create_api_response(success=True, message="Exploration job plan created successfully")

@router.post("/planning/create/development")
@authorize(role=[Role.KKKS])
async def create_planning_development(plan: schemas.CreateDevelopmentJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.DEVELOPMENT, plan, user)
    return create_api_response(success=True, message="Development job plan created successfully")

@router.post("/planning/create/workover")
@authorize(role=[Role.KKKS])
async def create_planning_workover(plan: schemas.CreateWorkoverJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WORKOVER, plan, user)
    return create_api_response(success=True, message="Workover job plan created successfully")

@router.post("/planning/create/wellservice")
@authorize(role=[Role.KKKS])
async def create_planning_wellservice(plan: schemas.CreateWellServiceJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WELLSERVICE, plan, user)
    return create_api_response(success=True, message="Well service job plan created successfully")

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

@router.get("/planning/view-raw/{job_id}")
def view_plan(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_plan = db.query(Job).get(job_id)
    if not job_plan:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    if job_plan.job_type == JobType.EXPLORATION:
        data = schemas.CreateExplorationJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.DEVELOPMENT:
        data = schemas.CreateDevelopmentJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.WORKOVER:
        data = schemas.CreateWorkoverJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.WELLSERVICE:
        data = schemas.CreateWellServiceJob.model_validate(job_plan, from_attributes=True)
    return create_api_response(success=True, message="Job plan retrieved successfully", data=data)

@router.put("/planning/update/{job_id}")
def update_planning_exploration(
    job_id: str,
    plan: Union[schemas.CreateExplorationJob, schemas.CreateDevelopmentJob, schemas.CreateWorkoverJob, schemas.CreateWellServiceJob],
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Any:
    crud.update_job_plan(db, job_id, plan, user)
    return create_api_response(success=True, message="Job Updated Successfully")

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

@router.get("/wrm-data/{actual_job_id}", response_model=Union[schemas.ActualExplorationUpdate, schemas.ActualDevelopmentUpdate, schemas.ActualWorkoverUpdate, schemas.ActualWellServiceUpdate])
async def read_wrm_data(
    actual_job_id: str,
    model_type: str = Query(..., description="Type of actual data (exploration, development, workover, wellservice)"),
    db: Session = Depends(get_db)
):
    model_map = {
        "exploration": models.ActualExploration,
        "development": models.ActualDevelopment,
        "workover": models.ActualWorkover,
        "wellservice": models.ActualWellService
    }

    if model_type not in model_map:
        raise HTTPException(status_code=400, detail="Invalid model type")

    model = model_map[model_type]
    wrm_data = crud.get_wrm_data_by_job_id(db, actual_job_id, model)

    if wrm_data is None:
        raise HTTPException(status_code=404, detail=f"WRM data not found for {model_type} with actual_job_id {actual_job_id}")

    return wrm_data

@router.get("/job-issues/{job_id}", response_model=List[schemas.JobIssueResponse])
def read_job_issues(job_id: str, db: Session = Depends(get_db)):
    job_issues = crud.get_wrmissues_data_by_job_id(db, job_id)
    if job_issues is None:
        raise HTTPException(status_code=404, detail="Job issues not found")
    return job_issues

@router.get("/drilling-operations/pyenum", response_model=List[schemas.DrillingOperationResponse])
async def list_drilling_operations():
    return [
        schemas.DrillingOperationResponse(operation=op, description=op.value)
        for op in models.DrillingOperation
    ]

@router.get("/bha/pyenum", response_model=List[schemas.BHAResponse])
async def list_bhacomponents():
    return [
        schemas.BHAResponse(bhacomponent=op)
        for op in models.BHAComponentType
    ]

# @router.get("/job-instances/{job_instance_id}/dates", response_model=List[str])
# def read_job_instance_dates(job_instance_id: str, db: Session = Depends(get_db)):
#     job_instance = crud.get_job_instance(db, job_instance_id)
#     if job_instance is None:
#         raise HTTPException(status_code=404, detail="Job instance not found")
#     return job_instance.get_job_date_list()

@router.get("/job-instances/{job_instance_id}/dates", response_model=List[schemas.ColoredDate])
def read_job_instance_dates(job_instance_id: str, db: Session = Depends(get_db)):
    job_instance = crud.get_job_instance(db, job_instance_id)
    if job_instance is None:
        raise HTTPException(status_code=404, detail="Job instance not found")
    
    date_list = job_instance.get_job_date_list()
    colored_dates = []
    
    for date_str in date_list:
        check_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        color = crud.get_date_color(db, job_instance_id, check_date)
        colored_dates.append(schemas.ColoredDate(date=date_str, color=color))
    
    return colored_dates

