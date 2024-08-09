from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import Role
from app.routers.auth.schemas import User
from app.routers.auth.utils import authorize, get_db, get_current_user
from app.routers.geometry import crud, schemas, models

router = APIRouter(prefix="/geometry", tags=["geometry"])

@router.post("/wk/create", response_model=schemas.WilayahKerjaSchema)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_wk(wk: schemas.WilayahKerjaSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_wk(db, wk)

@router.post("/field/create", response_model=schemas.FieldSchema)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_field(field: schemas.FieldSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.create_field(db, field)