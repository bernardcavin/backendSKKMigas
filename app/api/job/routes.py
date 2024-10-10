from venv import create
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Query
from pyparsing import C
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.core.security import authorize, get_db, get_current_user
from app.api.job import crud, models
from .schemas.dor import *
from .schemas.job import *
from app.api.job.models import JobType, Job
from app.core.schema_operations import create_api_response
from typing import Any, Union, List
from datetime import datetime

router = APIRouter(prefix="/job")

@router.post("/planning/upload-batch/exploration", summary="Upload Batch Job Exploration", tags=["Upload Batch Job"])
@authorize(role=[Role.KKKS])
async def upload_batch_exploration(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch(db, content, JobType.EXPLORATION, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/development", summary="Upload Batch Job Development", tags=["Upload Batch Job"])
@authorize(role=[Role.KKKS])
async def upload_batch_development(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch(db, content, JobType.DEVELOPMENT, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/workover", summary="Upload Batch Job Workover", tags=["Upload Batch Job"])
@authorize(role=[Role.KKKS])
async def upload_batch_workover(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch(db, content, JobType.WORKOVER, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/upload-batch/wellservice", summary="Upload Batch Job Well Service", tags=["Upload Batch Job"])
@authorize(role=[Role.KKKS])
async def upload_batch_wellservice(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = file.file.read()
    responses = crud.upload_batch(db, content, JobType.WELLSERVICE, user)
    return create_api_response(success=True, message="Job plan batch uploaded successfully")

@router.post("/planning/create/exploration", summary="Create Job Exploration (KKKS Only)" , tags=["Job Planning"])
@authorize(role=[Role.KKKS])
async def create_planning(plan: CreateExplorationJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.EXPLORATION, plan, user)
    return create_api_response(success=True, message="Exploration job plan created successfully")

@router.post("/planning/create/development", summary="Create Job Development (KKKS Only)", tags=["Job Planning"])
@authorize(role=[Role.KKKS])
async def create_planning_development(plan: CreateDevelopmentJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.DEVELOPMENT, plan, user)
    return create_api_response(success=True, message="Development job plan created successfully")

@router.post("/planning/create/workover", summary="Create Job Workover (KKKS Only)", tags=["Job Planning"])
@authorize(role=[Role.KKKS])
async def create_planning_workover(plan: CreateWorkoverJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WORKOVER, plan, user)
    return create_api_response(success=True, message="Workover job plan created successfully")

@router.post("/planning/create/wellservice", summary="Create Job Well Service (KKKS Only)", tags=["Job Planning"])
@authorize(role=[Role.KKKS])
async def create_planning_wellservice(plan: CreateWellServiceJob, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_id = crud.create_job_plan(db, JobType.WELLSERVICE, plan, user)
    return create_api_response(success=True, message="Well service job plan created successfully")

@router.delete('/planning/delete/{job_id}', summary="Delete Job Plan", tags=["Job Planning"])
@authorize(role=[Role.Admin, Role.KKKS])
async def delete_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    deleted = crud.delete_job_plan(job_id, db, user)
    if not deleted:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan deleted successfully")

@router.patch('/planning/approve/{job_id}', summary="Approve Job Plan (Admin Only)", tags=["Job Planning"])
@authorize(role=[Role.Admin])
async def approve_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    approved = crud.approve_job_plan(job_id, db, user)
    if not approved:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan approved successfully")

@router.patch('/planning/return/{job_id}', summary="Return Job Plan (Admin Only)", tags=["Job Planning"])
@authorize(role=[Role.Admin])
async def return_planning_exploration(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    returned = crud.return_job_plan(job_id, db, user)
    if not returned:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan returned successfully")

@router.get("/planning/get/{job_id}", summary="View Job Plan (Raw)", tags=["Job Planning"])
@authorize(role=[Role.Admin, Role.KKKS])
async def view_plan(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_plan = db.query(Job).get(job_id)
    if not job_plan:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    if job_plan.job_type == JobType.EXPLORATION:
        data = CreateExplorationJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.DEVELOPMENT:
        data = CreateDevelopmentJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.WORKOVER:
        data = CreateWorkoverJob.model_validate(job_plan, from_attributes=True)
    elif job_plan.job_type == JobType.WELLSERVICE:
        data = CreateWellServiceJob.model_validate(job_plan, from_attributes=True)
    return create_api_response(success=True, message="Job plan retrieved successfully", data=data)

@router.put("/planning/update/{job_id}", summary="Update Job Plan (KKKS Only)", tags=["Job Planning"])
@authorize(role=[Role.KKKS])
async def update_planning_exploration(
    job_id: str,
    plan: Union[CreateExplorationJob, CreateDevelopmentJob, CreateWorkoverJob, CreateWellServiceJob],
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Any:
    crud.update_job_plan(db, job_id, plan, user)
    return create_api_response(success=True, message="Job Updated Successfully")

@router.get('/planning/view/{job_id}', summary="View Job Plan", tags=["Job Planning"])
@authorize(role=[Role.Admin, Role.KKKS])
async def view_plan(job_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job_plan = crud.get_job_plan(job_id, db)
    if not job_plan:
        return create_api_response(success=False, message="Job plan not found", status_code=404)
    return create_api_response(success=True, message="Job plan retrieved successfully", data=job_plan)

#operation
@router.patch('/operation/operate/{job_id}', summary="Operate Job (KKKS Only)", tags=["Job Operation"])
@authorize(role=[Role.KKKS])
async def operate_job(job_id: str, surat_tajak: SuratTajakSchema, db: Session = Depends(get_db), user = Depends(get_current_user)):
    operated = crud.operate_job(job_id, surat_tajak, db)
    if not operated:
        return create_api_response(success=False, message="Job not found or operation failed", status_code=404)
    return create_api_response(success=True, message="Job operation started successfully")

#dor
@router.post("/operation/{job_id}/dor/create/", summary="Create Daily Operations Report by Job ID (KKKS Only)", tags=["Job Operation"])
async def create_daily_operations_report(job_id: str,report: DailyOperationsReportCreate, db: Session = Depends(get_db)):
    crud.create_daily_operations_report(db, job_id, report)
    return create_api_response(success=True, message="Daily Operations Report created successfully")

@router.get("/operation/{job_id}/dor/dates/", summary="Get Daily Operations Report Dates", tags=["Job Operation"])
async def get_daily_opeartions_report_dates(job_id: str, db: Session = Depends(get_db)):
    data = crud.get_dor_dates(db, job_id)
    return create_api_response(success=True, message="Daily Operations Report dates retrieved successfully", data=data)

@router.get("/operation/{job_id}/dor/{report_date}/get", summary="Get Daily Operations Report by Job ID and Report Date", tags=["Job Operation"])
async def get_daily_operations_report_by_job_id_and_date(job_id: str, report_date: date, db: Session = Depends(get_db)):
    dor = crud.get_dor_by_date(db, job_id, report_date)
    if dor is None:
        raise HTTPException(status_code=404, detail="Daily Operations Report not found")
    dor_output = DailyOperationsReportCreate.model_validate(dor)
    return create_api_response(success=True, message="Daily Operations Report retrieved successfully", data=dor_output)

@router.put("/operation/{job_id}/dor/{report_date}/edit/", summary="Edit Daily Operations Report identified by Job ID and Report Date (KKKS Only)", tags=["Job Operation"])
async def edit_daily_operations_report(job_id: str, report_date: date, report: DailyOperationsReportEdit, db: Session = Depends(get_db)):
    crud.edit_daily_operations_report(db, job_id, report_date, report)
    return create_api_response(success=True, message="Daily Operations Report edited successfully")

#issues
@router.get("/operation/{job_id}/issues/", summary="Get Job Issues (KKKS Only)", tags=["Job Operation"])
async def get_job_issues(
    job_id: str,
    db: Session = Depends(get_db)
) -> Any:
    data = crud.get_job_issues(db, job_id)
    return create_api_response(success=True, message="Job issues retrieved successfully", data=data)

@router.post("/operation/{job_id}/issues/create/", summary="Create Job Issue identified by Job ID (KKKS Only)", tags=["Job Operation"])
async def create_job_issue(
    job_id: str,
    job_issue: JobIssueCreate,
    db: Session = Depends(get_db)
) -> Any:
    crud.create_job_issue(db, job_id, job_issue)
    return create_api_response(success=True, message="Job issue created successfully")

@router.patch("/issues/{job_issue_id}/edit/", summary="Edit Job Issue identified by Job Issue ID (KKKS Only)", tags=["Job Operation"])
async def edit_job_issue(
    job_issue_id: str,
    job_issue: JobIssueEdit,
    db: Session = Depends(get_db)
) -> Any:
    crud.edit_job_issue(db, job_issue_id, job_issue)
    return create_api_response(success=True, message="Job issue created successfully")

@router.patch("/issues/{job_issue_id}/resolve", summary="Resolve Job Issue identified by Job Issue ID (KKKS Only)", tags=["Job Operation"])
async def resolve_job_issue(
    job_issue_id: str,
    db: Session = Depends(get_db)
) -> Any:
    crud.resolve_job_issue(db, job_issue_id)
    return create_api_response(success=True, message="Job issue resolved successfully")

#wrm
@router.get("/operation/{job_id}/wrm/requirements", summary="Get WRM Requirements (KKKS Only)", tags=["Job Operation"])
async def get_wrm_requirements(
    job_id: str,
    db: Session = Depends(get_db)
):
    data = crud.get_wrm_requirements(db, job_id)
    return create_api_response(success=True, message="WRM progress retrieved successfully", data=data)

@router.get("/operation/{job_id}/wrm/progress", summary="Get WRM Progress Cut by requirements (KKKS Only)", tags=["Job Operation"])
async def get_wrm_progress(
    job_id: str,
    db: Session = Depends(get_db)
):
    data = crud.get_wrm_progress(db, job_id)
    return create_api_response(success=True, message="WRM progress retrieved successfully", data=data)

@router.post("/operation/{job_id}/wrm/update", summary="Update WRM Progress (KKKS Only)", tags=["Job Operation"])
async def update_wrm(
    job_id: str,
    wrm_data: Union[ExplorationWRM, DevelopmentWRM, WorkoverWRM, WellServiceWRM],
    db: Session = Depends(get_db)
):
    crud.update_wrm(db, job_id, wrm_data)
    return create_api_response(success=True, message="WRM updated successfully")

@router.put("/operation/{job_id}/update", summary="Update Job Operation (Actual Job) (KKKS Only)", tags=["Job Operation"])
async def patch_actual_exploration_route(
    job_id: str,
    actual: Union[UpdateActualExploration, UpdateActualDevelopment, UpdateActualWorkover, UpdateActualWellService],
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    crud.update_operation(db, job_id, actual)
    return create_api_response(True, "Job operation updated successfully")

@router.get("/operation/{job_id}/validate", summary="Validate Job Operation before Finishing", tags=["Job Operation"])
async def validate_actual_operation(
    job_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = crud.get_job_operation_validations(db, job_id)
    return create_api_response(success=True, message="Validation Successful", data=data)

@router.get("/operation/{job_id}/finish", summary="Finish Job Operation", tags=["Job Operation"])
async def finish_actual_operation(
    job_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    crud.finish_operation(db, job_id)
    return create_api_response(success=True, message="Job Operation finished successfully")
    
#PPP
@router.patch("/ppp/{job_id}/propose", summary="Propose PPP (KKKS Only)", tags=["Job PPP"])
async def propose_ppp(job_id: str, proposal: ProposePPP, db: Session = Depends(get_db), user=Depends(get_current_user)):
    crud.propose_ppp(db, job_id, proposal)
    return create_api_response(True, "Propose PPP successfully")

@router.patch("/ppp/{job_id}/approve", summary="Approve PPP (Admin Only)", tags=["Job PPP"])
async def approve_ppp(job_id: str, approval: ApprovePPP, db: Session = Depends(get_db), user=Depends(get_current_user)):
    crud.approve_ppp(db, job_id, approval)
    return create_api_response(True, "PPP Approved successfully")
