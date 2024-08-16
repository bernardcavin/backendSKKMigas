from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import Role
from app.routers.auth.schemas import User
from app.routers.auth.utils import authorize, get_db, get_current_user
from app.routers.geometry import crud, schemas, models

router = APIRouter(prefix="/geometry", tags=["geometry"])

@router.post("/area/create", response_model=schemas.GetAreaSchema)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_area(area: schemas.CreateAreaSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_area(db, area)

@router.post("/field/create", response_model=schemas.GetFieldSchema)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_field(field: schemas.CreateFieldSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_field(db, field)

@router.post("/strat-unit/create", response_model=schemas.GetStratUnitSchema)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_strat_unit(strat_unit: schemas.CreateStratUnitSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_strat_unit(db, strat_unit)