from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.job.models import Job, JobType, PlanningStatus, OperationStatus
from app.api.job.schemas import PlanExploration, PlanDevelopment, PlanWell
from app.api.auth.schemas import GetUser
from app.core.schema_operations import parse_schema
from app.api.job.utils import create_gantt_chart, create_operation_plot, create_well_path
from app.api.visualize.schemas import VisualizeCasing
from app.api.visualize.routes import request_visualize_casing
from well_profile import load
import pandas as pd
from typing import Union

def create_job_plan(db: Session, job_type: JobType, plan: object, user):
    db_job = Job(**parse_schema(plan))
    db_job.kkks_id = user.kkks_id
    db_job.job_type = job_type
    db_job.date_proposed = datetime.now().date()
    db_job.planning_status = PlanningStatus.PROPOSED
    db_job.created_by_id = user.id
    db_job.time_created = datetime.now()
    db.add(db_job)
    db.commit()
    return db_job.id

def delete_job_plan(id: str, db: Session, user):
    db_job = db.query(Job).filter_by(id=id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job plan not found")
    if db_job.planning_status == PlanningStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Job is already approved")
    db.delete(db_job)
    db.commit()
    return {"message": "Job plan deleted successfully"}

def approve_job_plan(id: str, db: Session, user):
    db_job = db.query(Job).filter_by(id=id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job plan not found")
    db_job.planning_status = PlanningStatus.APPROVED
    db_job.date_approved = datetime.now().date()
    db_job.approved_by_id = user.id
    db.commit()
    return {"message": "Job plan approved successfully"}

def return_job_plan(id: str, remarks: str, db: Session, user):
    db_job = db.query(Job).filter_by(id=id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job plan not found")
    db_job.planning_status = PlanningStatus.RETURNED
    db_job.date_returned = datetime.now().date()
    db_job.returned_by_id = user.id
    db_job.remarks = remarks
    db.commit()
    return {"message": "Job plan returned successfully"}

def operate_job(id: str, db: Session, user):
    db_job = db.query(Job).filter_by(id=id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db_job.operation_status = OperationStatus.OPERATING
    db_job.date_started = datetime.now().date()
    db.commit()
    return {"message": "Job operation started successfully"}

def get_job_plan(id: str, db: Session) -> dict:
    db_job = db.query(Job).get(id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job plan not found")

    db_plan = _get_plan_from_job(db_job)
    db_well = _get_well_from_plan(db_plan)

    view_plan = {
        'operational': {
            "Tipe Pekerjaan": db_job.job_type,
            "KKKS": db_job.kkks.name,
            "Wilayah Kerja": db_job.area.name,
            "Lapangan": db_job.field.name,
            "Jenis Kontrak": db_job.contract_type.value,
            "Nomor AFE": db_job.afe_number,
            "Tahun WP&B": db_job.wpb_year,
            'Tanggal Diajukan': db_job.date_proposed,
            "Tanggal Mulai": db_plan.start_date,
            "Tanggal Selesai": db_plan.end_date,
            "Total Budget": db_plan.total_budget,
            "Nama Rig": db_plan.rig_name,
            "Tipe Rig": db_plan.rig_type,
            "RIG HP": db_plan.rig_horse_power,
            "Planning Status": db_job.planning_status,
        },
        'technical': {
            "UWI": db_well.uwi,
            "Nama Well": db_well.well_name,
            "Alias Well": db_well.alias_long_name,
            "Tipe Well": db_well.well_type,
            "Tipe Profil Well": db_well.well_profile_type,
            "Hidrokarbon Target": db_well.hydrocarbon_target,
            "Tipe Lingkungan": db_well.environment_type,
            "Longitude Permukaan": db_well.surface_longitude,
            "Latitude Permukaan": db_well.surface_latitude,
            "Longitude Bottom Hole": db_well.bottom_hole_longitude,
            "Latitude Bottom Hole": db_well.bottom_hole_latitude,
            "Maximum Inclination": db_well.maximum_inclination,
            "Azimuth": db_well.azimuth,
            "Nama Seismic Line": db_well.line_name,
            "Tanggal Tajak": db_well.spud_date,
            "Tanggal Selesai Drilling": db_well.final_drill_date,
            "Tanggal Komplesi": db_well.completion_date,
            "Elevasi Rotary Table": f'{db_well.rotary_table_elev} {db_well.rotary_table_elev_uom}',
            "Elevasi Kelly Bushing": f'{db_well.kb_elev} {db_well.kb_elev_uom}',
            "Elevasi Derrick Floor": f'{db_well.derrick_floor_elev} {db_well.derrick_floor_elev_uom}',
            "Elevasi Ground": f'{db_well.ground_elev} {db_well.ground_elev_uom}',
            "Mean Sea Level": f'{db_well.mean_sea_level} {db_well.mean_sea_level_uom}',
            "Kick Off Point": f'{db_well.kick_off_point} {db_well.kick_off_point_uom} from {db_well.depth_datum}',
            "Maximum TVD": f'{db_well.maximum_tvd} {db_well.maximum_tvd_uom} from {db_well.depth_datum}',
            "Final MD": f'{db_well.final_md} {db_well.final_md_uom} from {db_well.depth_datum}',
        }
    }

    job_wbs = db_plan.work_breakdown_structure
    view_plan['operational']['work_breakdown_structure'] = create_gantt_chart(
        [wbs.event for wbs in job_wbs],
        [wbs.start_date for wbs in job_wbs],
        [wbs.end_date for wbs in job_wbs]
    )

    job_operation_days = db_plan.job_operation_days
    view_plan['operational']['job_operation_days'] = create_operation_plot(
        [od.phase for od in job_operation_days],
        [od.operation_days for od in job_operation_days],
        [od.depth_in for od in job_operation_days],
        [od.depth_out for od in job_operation_days],
        [(db_job.job_plan.total_budget / len(job_operation_days)) for _ in job_operation_days]
    )

    casings = db_well.well_casing
    casing_schema = VisualizeCasing(
        names=[casing.description for casing in casings],
        top_depths=[casing.depth - casing.length for casing in casings],
        bottom_depths=[casing.depth for casing in casings],
        diameters=[casing.casing_outer_diameter for casing in casings]
    )
    view_plan['technical']['well_casing'] = request_visualize_casing(casing_schema)

    trajectory = db_well.well_trajectory
    well_profile_df = pd.DataFrame(load(trajectory.file.file_location).trajectory)
    view_plan['technical']['well_trajectory'] = create_well_path(well_profile_df, [casing.depth for casing in casings])

    return view_plan

def _get_well_from_plan(job: Union[PlanExploration, PlanDevelopment]) -> PlanWell:
    return job.well

def _get_plan_from_job(plan: Job) -> Union[PlanExploration, PlanDevelopment]:
    return plan.job_plan
