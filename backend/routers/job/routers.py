from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas
from backend.routers.job.models import JobType
from backend.utils.schema_operations import OutputSchema

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/planning/create/exploration", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_exploration(plan: schemas.ExplorationJobPlan, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db, JobType.EXPLORATION, plan, user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/development", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_development(plan: schemas.DevelopmentJobPlan, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db, JobType.DEVELOPMENT, plan, user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/workover", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_workover(plan: schemas.WorkoverJobPlan, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db, JobType.WORKOVER, plan, user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/wellservice", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_wellservice(plan: schemas.WellServiceJobPlan, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db, JobType.WELLSERVICE, plan, user)
    
    return OutputSchema(
        id=job_id
    )

@router.delete('/planning/delete/{job_id}')
@authorize(role=[Role.Admin])
async def delete_planning_exploration(job_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.delete_job_plan(job_id, db, user)

@router.patch('/planning/approve/{job_id}')
@authorize(role=[Role.Admin])
async def approve_planning_exploration(job_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.approve_job_plan(job_id, db, user)

@router.patch('/planning/return/{job_id}')
@authorize(role=[Role.Admin])
async def approve_planning_exploration(job_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.return_job_plan(job_id, db, user)

@router.get('/planning/view/{job_id}')
@authorize(role=[Role.Admin, Role.KKKS])
async def view_plan(job_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.get_job_plan(job_id, db)

@router.patch('/operations/operate/{job_id}')
@authorize(role=[Role.Admin])
async def operate_job(job_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.operate_job(job_id, db, user)


