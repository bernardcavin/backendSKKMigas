from sqlalchemy.orm import Session

from app.api.well.models import *
from app.api.well.schemas import *
from app.api.job.models import *
from app.api.job.schemas import *
from app.api.utils.models import *
from app.api.utils.schemas import *
from app.api.auth.schemas import GetUser

from app.core.schema_operations import parse_schema
import uuid

def create_well(db: Session, well: CreateExistingWell, user):

    db_well = ActualWell(
        **parse_schema(well)
    )
    
    db_well.kkks_id = user.kkks_id
    
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    
    return db_well.id

def get_wells(db: Session, kkks_id: str):
    # Ambil data WellInstance beserta relasi Area dan Lapangan
    get_wells = (
        db.query(ActualWell)
        .filter(WellInstance.kkks_id == kkks_id)
        .join(Area, WellInstance.area_id == Area.id, isouter=True)
        .join(Lapangan, WellInstance.field_id == Lapangan.id, isouter=True)
        .join(ActualWell, WellInstance.well_instance_id == ActualWell.id, isouter=True)
        .all()
    )

    wells_with_relations = [
        {
            "well_id": well.id,
            "well_name": well.well_name,
            "kkks_id": well.kkks_id,
            "area": well.area.name if well.area else None,
            "field": well.field.name if well.field else None,
            "well_status": well.well_status
        }
        for well in get_wells
    ]

    return wells_with_relations

def delete_wells(db:Session, wellactual_id:str):
    get_well=db.query(ActualWell).filter(ActualWell.id==wellactual_id).first()
    print(get_well)
    db.delete(get_well) 
    db.commit()
    return get_well

def edit_well(db:Session, wellactual_id:str, actual: UpdateActualWell):
    get_well=db.query(ActualWell).filter(ActualWell.id==wellactual_id).first()
    edit_well=ActualWell(**parse_schema(actual))
    db.commit()
    return edit_well
