from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_db, get_current_user
from app.api.well import crud, schemas
from app.core.schema_operations import create_api_response

router = APIRouter(prefix="/well", tags=["well"])

@router.post("/create")
@authorize(role=[Role.KKKS, Role.Admin])
async def create_well(well: schemas.CreateActualWell, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        well_id = crud.create_well(db, well, user)
        return create_api_response(success=True, message="Well created successfully")
    except Exception as e:
        return create_api_response(success=False, message="Failed to create well", status_code=500)