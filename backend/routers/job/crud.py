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
    
    db_plan.date_proposed = datetime.now().date()
    db_plan.status = PlanningStatus.PROPOSED
    
    db_plan.proposed_job.well.kkks_id = user.kkks_id
    db_plan.proposed_job.kkks_id = user.kkks_id
    
    db_plan.proposed_job.well.area_id = db_plan.proposed_job.area_id
    db_plan.proposed_job.well.field_id = db_plan.proposed_job.field_id
    
    db_plan.created_by_id = user.id
    db_plan.time_created = datetime.now()

    db.add(db_plan)
    db.commit()

    return db_plan.id

def validate_job_plan(id: str, db: Session, user: GetUser):

    db_plan = db.query(Planning).filter_by(id=id).one()
    
    db_plan.date_approved = datetime.now().date()
    db_plan.status = PlanningStatus.APPROVED
    db_plan.validated_by_id = user.id
    db_plan.validation_date = datetime.now().date()
    db.commit()
    
    return {
        'status': 'success',
    }
    
def _get_job_from_plan(job) -> Well:
    
    return job.well
    
def get_plan(id: str, db: Session) -> Planning:
    
    db_plan = db.query(Planning).filter_by(id=id).one()
    
    view_plan = db_plan.__dict__
    
    return db_plan
    
    
