from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_db, get_current_user
from app.api.spatial import crud, schemas
from app.core.schema_operations import create_api_response

router = APIRouter(prefix="/spatial", tags=["spatial"])

@router.post("/area/create")
@authorize(role=[Role.KKKS])
async def create_area(area: schemas.CreateAreaSchema, db: Session = Depends(get_db), user = Depends(get_current_user)):
    created_area = crud.create_area(db, area, user)
    if not created_area:
        return create_api_response(success=False, message="Failed to create area", status_code=400)
    return create_api_response(success=True, message="Area created successfully", data=created_area)

@router.post("/field/create")
@authorize(role=[Role.KKKS])
async def create_field(field: schemas.CreateFieldSchema, db: Session = Depends(get_db), user = Depends(get_current_user)):
    created_field = crud.create_field(db, field)
    if not created_field:
        return create_api_response(success=False, message="Failed to create field", status_code=400)
    return create_api_response(success=True, message="Field created successfully", data=created_field)

@router.post("/strat-unit/create")
@authorize(role=[Role.KKKS])
async def create_strat_unit(strat_unit: schemas.CreateStratUnitSchema, db: Session = Depends(get_db), user = Depends(get_current_user)):
    created_strat_unit = crud.create_strat_unit(db, strat_unit)
    if not created_strat_unit:
        return create_api_response(success=False, message="Failed to create stratigraphic unit", status_code=400)
    return create_api_response(success=True, message="Stratigraphic unit created successfully", data=created_strat_unit)
