from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas, models

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/create/pengajuan/drilling", response_model=schemas.GetPengajuanDrilling)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_pengajuan_drilling(job: schemas.CreatePengajuanDrilling, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.create_pengajuan_drilling(db, job, user)

@router.post("/create/pengajuan/wows", response_model=schemas.GetPengajuanWOWS)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_pengajuan_drilling(job: schemas.CreatePengajuanWOWS, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.create_pengajuan_wows(db, job, user)