from sqlalchemy.orm import Session

from app.routers.job.models import *
from app.routers.job.schemas import *
from app.routers.well.crud import *
from app.routers.auth.schemas import GetUser

from typing import Union

def create_drilling_job(db: Session, drilling: CreateDrillingJob, user: GetUser):

    db_well = create_well(
        db,
        drilling.planned_well,
        DataPhase.PLAN
    )

    # Create the main Drilling record
    db_drilling = Drilling(
        #job data
        date_created=datetime.now(),
        kkks_id=user.kkks_id,
        field_id=drilling.field_id,
        contract_type=drilling.contract_type,
        job_type=drilling.job_type,
        afe_number=drilling.afe_number,
        wpb_year=drilling.wpb_year,
        plan_start=drilling.plan_start,
        plan_end=drilling.plan_end,
        plan_total_budget=drilling.plan_total_budget,
        rig_name=drilling.rig_name,
        rig_type=drilling.rig_type,
        rig_horse_power=drilling.rig_horse_power,
        created_by_id=user.id,

        #drilling data
        planned_well_id=db_well.id,
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

def create_wows_job(db: Session, wows: CreateWOWSJob, user: GetUser):

    db_well = create_well(
        db,
        wows.well,
        DataPhase.ACTUAL
    )

    # Create the main Drilling record
    db_wows = WOWS(

        #job data
        date_created=datetime.now(),
        kkks_id=user.kkks_id,
        field_id=wows.field_id,
        contract_type=wows.contract_type,
        job_type=wows.job_type,
        afe_number=wows.afe_number,
        wpb_year=wows.wpb_year,
        plan_start=wows.plan_start,
        plan_end=wows.plan_end,
        plan_total_budget=wows.plan_total_budget,
        rig_name=wows.rig_name,
        rig_type=wows.rig_type,
        rig_horse_power=wows.rig_horse_power,
        created_by_id=user.id,

        #wows data

        wows_class = wows.wows_class,
        well_id = db_well.id,
        job_category= wows.job_category,
        
        #current
        current_oil=wows.current_oil,
        current_gas=wows.current_gas,
        current_condensate=wows.current_condensate,
        
        current_oil_water_cut=wows.current_oil_water_cut,
        current_gas_water_cut=wows.current_gas_water_cut,
        current_condensate_water_cut=wows.current_condensate_water_cut,
        
        # target
        target_oil=wows.target_oil,
        target_gas=wows.target_gas,
        target_condensate=wows.target_condensate,
        
        target_oil_water_cut=wows.target_oil_water_cut,
        target_gas_water_cut=wows.target_gas_water_cut,
        target_condensate_water_cut=wows.target_condensate_water_cut,
    )

    db.add(db_wows)
    db.commit()

    wows_id = db_wows.id

    # Add related Job Activities
    for activity in wows.job_activity:
        db_activity = JobActivity(
            wows_id=wows_id,
            **activity.model_dump()
        )
        db.add(db_activity)

    # Add related Budgets
    for budget in wows.budget:
        db_budget = Budget(
            wows_id=wows_id,
            **budget.model_dump()
        )
        db.add(db_budget)

    # Add related Work Breakdown Structures
    for wbs in wows.work_breakdown_structure:
        db_wbs = WorkBreakdownStructure(
            wows_id=wows_id,
            **wbs.model_dump()
        )
        db.add(db_wbs)

    # Add related wows Hazards
    for hazard in wows.drilling_hazard:
        db_hazard = DrillingHazard(
            wows_id=wows_id,
            **hazard.model_dump()
        )
        db.add(db_hazard)

    # Add related Job Documents
    for document in wows.job_documents:
        db_document = JobDocument(
            wows_id=wows_id,
            **document.model_dump()
        )
        db.add(db_document)

    db.commit()
    db.refresh(db_wows)
    return db_wows

def create_pengajuan_drilling(db: Session, pengajuan: CreatePengajuanDrilling, user: GetUser):
    db_job = create_drilling_job(
        db,
        pengajuan.job,
        user
    )
    db_pengajuan = Pengajuan(
        job_id = db_job.id,
        tanggal_diajukan = datetime.now(),
        status = StatusPengajuan.DIAJUKAN,
    )
    db.add(db_pengajuan)
    db.commit()
    db.refresh(db_pengajuan)
    return db_pengajuan

def create_pengajuan_wows(db: Session, pengajuan: CreatePengajuanWOWS, user: GetUser):
    db_job = create_wows_job(
        db,
        pengajuan.job,
        user
    )
    db_pengajuan = Pengajuan(
        job_id = db_job.id,
        tanggal_diajukan = datetime.now(),
        status = StatusPengajuan.DIAJUKAN,
    )
    db.add(db_pengajuan)
    db.commit()
    db.refresh(db_pengajuan)
    return db_pengajuan

# def create_job_activity(db: Session, job_id: str, job_log: CreateJobActivity):
    
#     db_job_log = JobActivity(
#         **job_log.model_dump(), job_id = job_id
#     )
#     db.add(db_job_log)
#     db.commit()
#     db.refresh(db_job_log)
#     return db_job_log




