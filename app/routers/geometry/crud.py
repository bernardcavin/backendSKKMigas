from sqlalchemy.orm import Session

from app.routers.geometry.models import *
from app.routers.geometry.schemas import WilayahKerjaSchema, FieldSchema

def create_wk(db: Session, wk: WilayahKerjaSchema ):
    
    db_wk = Area(
        **wk.model_dump()
    )
    db.add(db_wk)
    db.commit()
    db.refresh(db_wk)
    return db_wk

def create_field(db: Session, field: FieldSchema ):
    
    db_field = Field(
        **field.model_dump()
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field