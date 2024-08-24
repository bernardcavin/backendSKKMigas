from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session

from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.auth.schemas import GetUser

from backend.utils.schema_operations import parse_schema
from backend.utils.db_operations import model_to_dict
from backend.routers.job.utils import create_gantt_chart

def create_job_plan(db: Session, plan: object, user: GetUser):

    db_plan = Planning(
        **parse_schema(plan)
    )
    
    db_plan.date_proposed = datetime.now().date()
    db_plan.status = PlanningStatus.PROPOSED
    
    db_plan.proposed_job.job_instance_type = JobInstanceType.INITIAL_PROPOSAL
    
    db_plan.proposed_job.well.kkks_id = user.kkks_id
    db_plan.proposed_job.kkks_id = user.kkks_id
    
    db_plan.proposed_job.well.area_id = db_plan.proposed_job.area_id
    db_plan.proposed_job.well.field_id = db_plan.proposed_job.field_id
    
    db_plan.proposed_job.well.data_phase = DataPhase.PROPOSED
    
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
    
def _get_well_from_job(job: Union[Exploration, Development]) -> Well:
    
    return job.well

def _get_job_from_plan(plan: Planning) -> Union[Exploration, Development]:
    
    return plan.proposed_job

    
def get_plan(id: str, db: Session) -> Planning:
    
    db_plan = db.query(Planning).get(id)
    
    db_job = _get_job_from_plan(db_plan)
    db_well = _get_well_from_job(db_job)
    
    view_plan = model_to_dict(db_plan)
    view_plan['operational'] = model_to_dict(db_job)
    
    #work breakdown structure
    job_wbs = db_job.work_breakdown_structure
    
    events = [wbs.event for wbs in job_wbs]
    plan_start_dates = [wbs.start_date for wbs in job_wbs]
    plan_end_dates = [wbs.end_date for wbs in job_wbs]
    
    wbs = create_gantt_chart(
        events,
        plan_start_dates,
        plan_end_dates
    )
    
    view_plan['work_breakdown_structure'] = wbs
    
    view_plan['technical'] = model_to_dict(db_well)
    
    return view_plan
    
    
