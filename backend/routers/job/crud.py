from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session

from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.auth.schemas import GetUser

from backend.utils.schema_operations import parse_schema
from backend.utils.db_operations import model_to_dict
from backend.routers.job.utils import create_gantt_chart, create_operation_plot, create_well_path
from backend.routers.visualize.schemas import VisualizeCasing
from backend.routers.visualize.routers import request_visualize_casing

from well_profile import load
import pandas as pd

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
    view_plan['technical'] = model_to_dict(db_well)
    
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
    
    #job operation days
    job_operation_days = db_job.job_operation_days
    
    events = [od.phase for od in job_operation_days]
    depth_in = [od.depth_in for od in job_operation_days]
    depth_out = [od.depth_out for od in job_operation_days]
    operation_days = [od.operation_days for od in job_operation_days]
    daily_costs = [(db_job.total_budget/len(job_operation_days)) for od in job_operation_days]
    
    operation_days = create_operation_plot(
        events,
        operation_days,
        depth_in,
        depth_out,
        daily_costs
    )
    
    #casing
    casings = db_well.well_casing
    
    casing_end_depths = [
        casing.depth for casing in casings
    ]
    
    casing_names = [
        casing.description for casing in casings
    ]
    
    casing_top_depths = [
        casing.depth-casing.length for casing in casings
    ]
    
    casing_diameters = [
        casing.casing_outer_diameter for casing in casings
    ]
    
    casing_schema = VisualizeCasing(
        names = casing_names,
        top_depths = casing_top_depths,
        bottom_depths = casing_end_depths,
        diameters = casing_diameters,
    )
    
    view_plan['well_casing'] = request_visualize_casing(
        casing_schema
    )
    
    #trajectory
    trajectory = db_well.well_trajectory
    
    well_profile = load(trajectory.file.file_location)
    well_profile_df = pd.DataFrame(well_profile.trajectory)

    well_profile_plot = create_well_path(
        well_profile_df,
        casing_end_depths
    )
    
    view_plan['well_trajectory'] = well_profile_plot
    
    view_plan['job_operation_days'] = operation_days
    
    return view_plan
    
    
