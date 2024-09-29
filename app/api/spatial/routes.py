from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.auth.models import *
from app.api.spatial.models import *
from app.api.spatial.schemas import *
from app.api.well.models import *
from app.api.well.schemas import *
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_db, get_current_user
from app.api.spatial import crud, schemas
from app.core.schema_operations import create_api_response
from typing import List

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

# @router.post("/strat-unit/create")
# @authorize(role=[Role.KKKS])
# async def create_strat_unit(strat_unit: schemas.CreateStratUnitSchema, db: Session = Depends(get_db), user = Depends(get_current_user)):
#     created_strat_unit = crud.create_strat_unit(db, strat_unit)
#     if not created_strat_unit:
#         return create_api_response(success=False, message="Failed to create stratigraphic unit", status_code=400)
#     return create_api_response(success=True, message="Stratigraphic unit created successfully", data=created_strat_unit)

@router.get("/api/areas", response_model=List[AreaResponse])
def get_areas(db: Session = Depends(get_db)):
    areas = db.query(Area.id, Area.name).all()
    return areas

@router.get("/api/lapangan", response_model=List[LapanganResponse])
def get_areas(db: Session = Depends(get_db)):
    lapangan = db.query(Lapangan.id, Lapangan.name).all()
    return lapangan

@router.get("/api/well-instance", response_model=List[WellInstanceResponse])
def get_well_instances(db: Session = Depends(get_db)):
    well_instances = (
        db.query(WellInstance.well_instance_id, WellInstance.well_name)
        .filter(WellInstance.well_phase == "actual")
        .all()
    )
    return [
        WellInstanceResponse(id=well_instance_id, well_name=well_name)
        for well_instance_id, well_name in well_instances
    ]

# @router.get("/api/strat-units/{area_id}", response_model=List[StratUnitResponse])
# def get_strat_units_by_area(area_id: str, db: Session = Depends(get_db)):
#     strat_units = (
#         db.query(StratUnit)
#         .filter(StratUnit.area_id == area_id)
#         .all()
#     )
    
#     if not strat_units:
#         raise HTTPException(status_code=404, detail="No strat units found for this area")
    
#     return [
#         StratUnitResponse(
#             id=unit.id,
#             strat_unit_info=f"{unit.strat_unit_name} ({unit.strat_petroleum_system.name})"
#         )
#         for unit in strat_units
#     ]

