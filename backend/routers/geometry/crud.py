from sqlalchemy.orm import Session

from backend.routers.geometry.models import *
from backend.routers.geometry.schemas import *
from backend.routers.auth.schemas import GetUser

def create_area(db: Session, wk: CreateAreaSchema, user: GetUser):
    
    db_area = Area(
        **wk.model_dump(), kkks_id = user.kkks_id
    )
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def create_field(db: Session, field: CreateFieldSchema):
    
    db_field = Field(
        **field.model_dump()
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

def create_strat_unit(db: Session, strat_unit: CreateStratUnitSchema):
    
    db_strat_unit = StratUnit(
        **strat_unit.model_dump()
    )
    db.add(db_strat_unit)
    db.commit()
    db.refresh(db_strat_unit)
    return db_strat_unit