from sqlalchemy.orm import Session

from app.routers.geometry.models import *
from app.routers.geometry.schemas import *

def create_area(db: Session, wk: CreateAreaSchema):
    
    db_area = Area(
        **wk.model_dump()
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

def create_strat_unit(db: Session, field: CreateStratUnitSchema):
    
    db_strat_unit = Field(
        **field.model_dump()
    )
    db.add(db_strat_unit)
    db.commit()
    db.refresh(db_strat_unit)
    return db_strat_unit