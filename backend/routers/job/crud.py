from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

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

def create_job_plan(db: Session, job_type: JobType, plan: object, user: GetUser):

    db_job = Job(
        **parse_schema(plan)
    )
    
    db_job.kkks_id = user.kkks_id
    db_job.job_type = job_type
    db_job.date_proposed = datetime.now().date()
    db_job.planning_status = PlanningStatus.PROPOSED
    
    db_job.created_by_id = user.id
    db_job.time_created = datetime.now()

    db.add(db_job)
    db.commit()

    return db_job.id

def delete_job_plan(id: str, db: Session, user: GetUser):

    db_job = db.query(Job).filter_by(id=id).one()
    
    if db_job.planning_status == PlanningStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Job is already approved")
    
    db.delete(db_job)
    db.commit()
    
    return {
        'status': 'success',
    }

def approve_job_plan(id: str, db: Session, user: GetUser):

    db_job = db.query(Job).filter_by(id=id).one()
    
    db_job.planning_status = PlanningStatus.APPROVED
    db_job.date_approved = datetime.now().date()
    db_job.approved_by_id = user.id
    db_job.remarks = None
    
    db.commit()
    
    return {
        'status': 'success',
    }

def return_job_plan(id: str, remarks: str, db: Session, user: GetUser):

    db_job = db.query(Job).filter_by(id=id).one()
    
    db_job.planning_status = PlanningStatus.RETURNED
    db_job.date_returned = datetime.now().date()
    db_job.returned_by_id = user.id
    db_job.remarks = remarks
    
    db.commit()
    
    return {
        'status': 'success',
    }

def operate_job(id: str, db: Session, user: GetUser):

    db_job = db.query(Job).filter_by(id=id).one()
    
    db_job.operation_status = OperationStatus.OPERATING
    db_job.date_started = datetime.now().date()
    
    db.commit()
    
    return {
        'status': 'success',
    }

def _get_well_from_plan(job: Union[PlanExploration, PlanDevelopment]) -> PlanWell:
    
    return job.well

def _get_plan_from_job(plan: Job) -> Union[PlanExploration, PlanDevelopment]:
    
    return plan.job_plan
    
def get_job_plan(id: str, db: Session) -> Job:
    
    db_job = db.query(Job).get(id)
    
    db_plan = _get_plan_from_job(db_job)
    db_well = _get_well_from_plan(db_plan)
    
    view_plan = {}
    
    view_plan['operational'] = {
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
    }

    view_plan["technical"] = {
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
    
    #work breakdown structure
    job_wbs = db_plan.work_breakdown_structure
    
    events = [wbs.event for wbs in job_wbs]
    plan_start_dates = [wbs.start_date for wbs in job_wbs]
    plan_end_dates = [wbs.end_date for wbs in job_wbs]
    
    wbs = create_gantt_chart(
        events,
        plan_start_dates,
        plan_end_dates
    )
    
    view_plan['operational']['work_breakdown_structure'] = wbs
    
    #job operation days
    job_operation_days = db_plan.job_operation_days
    
    events = [od.phase for od in job_operation_days]
    depth_in = [od.depth_in for od in job_operation_days]
    depth_out = [od.depth_out for od in job_operation_days]
    operation_days = [od.operation_days for od in job_operation_days]
    daily_costs = [(db_job.job_plan.total_budget/len(job_operation_days)) for od in job_operation_days]
    
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
    
    view_plan['technical']['well_casing'] = request_visualize_casing(
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
    
    view_plan['technical']['well_trajectory'] = well_profile_plot
    
    view_plan['operational']['job_operation_days'] = operation_days
    
    return view_plan


def time_to_datetime(t: time) -> datetime:
    return datetime.combine(date.today(), t)

def datetime_to_time(dt: datetime) -> time:
    return dt.time()

# In your CRUD operations
def create_daily_operations_report(db: Session, report: DailyOperationsReportCreate):
    db_report = DailyOperationsReport(**report.dict(exclude={'time_breakdowns', 'personnel', 'Incidents', 'bit_records'}))
    
    for tb in report.time_breakdowns:
        start_datetime = datetime.combine(report.report_date, tb.start_time)
        end_datetime = datetime.combine(report.report_date, tb.end_time)
        
        # If end_time is earlier than start_time, assume it's the next day
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)
        
        db_time_breakdown = TimeBreakdown(
            start_time=start_datetime.replace(microsecond=0),
            end_time=end_datetime.replace(microsecond=0),
            start_measured_depth=tb.start_measured_depth,
            end_measured_depth=tb.end_measured_depth,
            category=tb.category,
            p=tb.p,
            npt=tb.npt,
            code=tb.code,
            operation=tb.operation
        )
        db_report.time_breakdowns.append(db_time_breakdown)
    
    for p in report.personnel:
        db_personnel = Personnel(
            company=p.company,
            people=p.people
        )
        db_report.personnel.append(db_personnel)
    
    for incident in report.Incidents:
        db_incident = Incident(
            incidents_time=incident.incidents_time,
            incident=incident.incident,
            incident_type=incident.incident_type,
            comments=incident.comments
        )
        db_report.Incidents.append(db_incident)

    for bit_record in report.bit_records:
        db_bit_record = BitRecord(
            bit_size=bit_record.bit_size,
            manufacturer=bit_record.manufacturer,
            iadc_code=bit_record.iadc_code,
            jets=bit_record.jets,
            serial=bit_record.serial,
            depth_out=bit_record.depth_out,
            depth_in=bit_record.depth_in,
            meterage=bit_record.meterage,
            bit_hours=bit_record.bit_hours,
            nozzels=bit_record.nozzels,
            dull_grade=bit_record.dull_grade
        )
        db_report.bit_records.append(db_bit_record)
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return {"data": db_report, "status": 200}



