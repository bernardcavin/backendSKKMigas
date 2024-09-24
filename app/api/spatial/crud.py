from sqlalchemy.orm import Session

from app.api.spatial.models import *
from app.api.spatial.schemas import *
from app.api.auth.schemas import GetUser

def create_area(db: Session, wk: CreateAreaSchema, user):
    
    db_area = Area(
        **wk.model_dump(), kkks_id = user.kkks_id
    )
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def create_field(db: Session, field: CreateFieldSchema):
    
    db_field = Lapangan(
        **field.model_dump()
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

# def create_strat_unit(db: Session, strat_unit: CreateStratUnitSchema):
    
#     db_strat_unit = StratUnit(
#         **strat_unit.model_dump()
#     )
#     db.add(db_strat_unit)
#     db.commit()
#     db.refresh(db_strat_unit)
#     return db_strat_unit
