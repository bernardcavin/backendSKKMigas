from sqlalchemy.orm import Session

from app.routers.job.models import *
from app.routers.job.schemas import *
from app.routers.well.crud import *

from typing import Union

def create_drilling(db: Session, drilling: CreateDrilling):
    # Create the main Drilling record
    db_drilling = Drilling(
        date_created=drilling.date_created,
        last_edited=drilling.last_edited,
        kkks_id=drilling.kkks_id,
        field_id=drilling.field_id,
        contract_type=drilling.contract_type,
        job_type=drilling.job_type,
        afe_number=drilling.afe_number,
        wpb_year=drilling.wpb_year,
        plan_start=drilling.plan_start,
        plan_end=drilling.plan_end,
        plan_total_budget=drilling.plan_total_budget,
        actual_start=drilling.actual_start,
        actual_end=drilling.actual_end,
        actual_total_budget=drilling.actual_total_budget,
        rig_name=drilling.rig_name,
        rig_type=drilling.rig_type,
        rig_horse_power=drilling.rig_horse_power,
        created_by_id=drilling.created_by_id,
        planned_well_id=drilling.planned_well_id.id,  # Assuming GetWell ID is used
    )
    
    db.add(db_drilling)
    db.commit()

    drilling_id = db_drilling.id

    # Add related Job Activities
    for activity in drilling.job_activity:
        db_activity = JobActivity(
            drilling_id=drilling_id,
            **activity.model_dump()
        )
        db.add(db_activity)

    # Add related Budgets
    for budget in drilling.budget:
        db_budget = Budget(
            drilling_id=drilling_id,
            **budget.model_dump()
        )
        db.add(db_budget)

    # Add related Work Breakdown Structures
    for wbs in drilling.work_breakdown_structure:
        db_wbs = WorkBreakdownStructure(
            drilling_id=drilling_id,
            **wbs.model_dump()
        )
        db.add(db_wbs)

    # Add related Drilling Hazards
    for hazard in drilling.drilling_hazard:
        db_hazard = DrillingHazard(
            drilling_id=drilling_id,
            **hazard.model_dump()
        )
        db.add(db_hazard)

    # Add related Job Documents
    for document in drilling.job_documents:
        db_document = JobDocument(
            drilling_id=drilling_id,
            **document.model_dump()
        )
        db.add(db_document)

    db.commit()
    db.refresh(db_drilling)
    return db_drilling

def create_job_activity(db: Session, job_id: str, job_log: CreateJobActivity):
    
    db_job_log = JobActivity(
        **job_log.model_dump(), job_id = job_id
    )
    db.add(db_job_log)
    db.commit()
    db.refresh(db_job_log)
    return db_job_log

# def create_pengajuan(db: Session, job_id: str, job_log: CreateJobActivity)
