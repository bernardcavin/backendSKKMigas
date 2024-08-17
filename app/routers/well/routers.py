from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import Role
from app.routers.auth.schemas import GetUser
from app.routers.auth.utils import authorize, get_db, get_current_user
from app.routers.well import crud, schemas, models

router = APIRouter(prefix="/well", tags=["well"])

@router.post("/create", response_model=schemas.GetWell)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_well(well: schemas.CreateWell, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    return crud.create_well(db, well, user)
