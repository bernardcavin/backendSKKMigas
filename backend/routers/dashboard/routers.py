from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas, models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.post("/job-type")
@authorize(role=[Role.KKKS, Role.Admin])
async def create_area(db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):

    exploration = db.query(func.count(models.Drilling.id)).filter(models.Drilling.drilling_class == models.DrillingClass.EXPLORATION).scalar()
    development = db.query(func.count(models.Drilling.id)).filter(models.Drilling.drilling_class == models.DrillingClass.DEVELOPMENT).scalar()

    return {
        'EXPLORATION':exploration,
        'DEVELOPMENT':development
    }