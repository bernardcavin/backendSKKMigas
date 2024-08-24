from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.well import crud, schemas
from backend.utils.schema_operations import OutputSchema

router = APIRouter(prefix="/well", tags=["well"])

@router.post("/create", response_model=OutputSchema)
@authorize(role=[Role.KKKS])
async def create_well(well: schemas.CreateWell, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    well_id = crud.create_well(db, well, user)
    
    return OutputSchema(id = well_id)
