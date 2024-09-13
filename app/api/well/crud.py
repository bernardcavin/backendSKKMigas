from sqlalchemy.orm import Session

from app.api.well.models import *
from app.api.well.schemas import *
from app.api.auth.schemas import GetUser

from app.core.schema_operations import parse_schema
import uuid

def create_well(db: Session, well: CreatePlanWell, user):

    db_well = ActualWell(
        **parse_schema(well)
    )
    
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    
    return db_well.id