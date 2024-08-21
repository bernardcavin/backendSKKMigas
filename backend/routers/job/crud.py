from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session

from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.auth.schemas import GetUser

from backend.utils.schema_operations import parse_schema

def create_job_plan(db: Session, plan: object, user: GetUser):

    db_plan = Planning(
        **parse_schema(plan)
    )

    db.add(db_plan)
    db.commit()

    return db_plan.id

def validate_exploration_plan(id: str, db: Session, validation: CreateExploration, user: GetUser):

    db_plan = db.query(Planning).filter_by(id=id).one()
    
    db_plan.approved_job = Exploration(
        **parse_schema(validation)
    )
    
    db_plan.date_approved = datetime.now().date()
    db_plan.status = PlanningStatus.APPROVED
    db_plan.validated_by_id = user.id
    db_plan.validation_date = datetime.now().date()
    db_plan.
    
    db.commit()
    
    return {
        'status': 'success',
    }
    
    
