from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.core.security import authorize, get_db, get_current_user
from app.api.well import crud, schemas
from app.core.schema_operations import create_api_response

router = APIRouter(prefix="/well", tags=["Well"])

@router.post("/create")
@authorize(role=[Role.KKKS, Role.Admin])
async def create_well(well: schemas.CreateActualWell, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        well_id = crud.create_well(db, well, user)
        return create_api_response(success=True, message="Well created successfully")
    except Exception as e:
        return create_api_response(success=False, message="Failed to create well", status_code=500)
    
@router.get("/wells/")
def read_wells(kkks_id: str, db: Session = Depends(get_db)):
    """
    Endpoint untuk mengambil data `well_name`, `field`, `area`, dan `well_status` berdasarkan `kkks_id`.
    
    Parameters:
    - `kkks_id` (str): ID KKKS yang akan digunakan untuk filter data.
    
    Returns:
    - List of dictionaries dengan format `well_name`, `field`, `area`, dan `well_status`.
    """
    wells = crud.get_wells(db, kkks_id)
    if not wells:
        raise HTTPException(status_code=404, detail="Data wells not found")
    return wells

@router.delete("/wells/{wellactual_id}")
# @authorize(role=[Role.KKKS, Role.Admin])
async def delete_well(wellactual_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_wells(db, wellactual_id,)
    if not deleted:
        return create_api_response(success=False, message="Well not found", status_code=404)
    return create_api_response(success=True, message="Well deleted successfully")

@router.patch("/edit_wells/{wellactual_id}")
async def edit_well(wellactual_id: str, actual: schemas.UpdateActualWell, db: Session = Depends(get_db)):
    edited = crud.edit_well(db, wellactual_id, actual)
    if not edited:
        return create_api_response(success=False, message="Well not found", status_code=404)
    return create_api_response(success=True, message="Well edited successfully")