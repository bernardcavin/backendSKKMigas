# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.routers.auth.models import Role
# from app.routers.auth.schemas import User
# from app.routers.auth.utils import authorize, get_db, get_current_user
# from app.routers.job import crud, schemas, models

# router = APIRouter(prefix="/job", tags=["job"])

# @router.post("/create", response_model=schemas.Job)
# @authorize(role=[Role.Admin, Role.KKKS])
# async def create_job(job: schemas.Job, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     return crud.create_job(db, job)

# @router.post("/create-log", response_model=schemas.Job)
# @authorize(role=[Role.Admin, Role.KKKS])
# async def create_log(job_log: schemas.LogPekerjaanSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     return crud.create_job_log(db, job_log)