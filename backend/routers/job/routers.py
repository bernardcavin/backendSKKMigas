from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas
from backend.utils.schema_operations import OutputSchema

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/planning/create/exploration", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_exploration(plan: schemas.CreateExplorationPlanning, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db,plan,user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/development", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_development(plan: schemas.CreateDevelopmentPlanning, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db,plan,user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/workover", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_workover(plan: schemas.CreateWorkoverPlanning, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db,plan,user)
    
    return OutputSchema(
        id=job_id
    )

@router.post("/planning/create/wellservice", response_model=OutputSchema)
@authorize(role=[Role.Admin,Role.KKKS])
async def create_planning_wellservice(plan: schemas.CreateWellServicePlanning, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    job_id = crud.create_job_plan(db,plan,user)
    
    return OutputSchema(
        id=job_id
    )

@router.patch('/planning/validate/{plan_id}')
@authorize(role=[Role.Admin])
async def validate_planning_exploration(plan_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.validate_job_plan(plan_id, db, user)

@router.get('/planning/view/{plan_id}')
@authorize(role=[Role.Admin])
async def view_plan(plan_id: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.get_plan(plan_id, db)