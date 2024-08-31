from sqlalchemy.orm import Session

from backend.routers.well.models import *
from backend.routers.well.schemas import *
from backend.routers.auth.schemas import GetUser

from backend.utils.schema_operations import parse_schema
import uuid

def create_well(db: Session, well: CreatePlanWell, user: GetUser):

    db_well = ActualWell(
        **parse_schema(well)
    )
    
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    
    return db_well.id