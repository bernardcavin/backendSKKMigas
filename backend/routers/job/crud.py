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
    
    db_plan.proposed_job.well.well_instance_type = WellInstanceType.INITIAL_PROPOSAL
    
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
    data_operational = model_to_dict(db_job)
    data_teknis = model_to_dict(db_well)
    
    view_plan['operational'] = {
        "Tipe Pekerjaan": data_operational["job_type"],
        "KKKS": db_plan.proposed_job.kkks.nama_kkks,
        "Wilayah Kerja": db_plan.proposed_job.area.area_name,
        "Lapangan": db_plan.proposed_job.field.field_name,
        "Jenis Kontrak": data_operational["contract_type"],
        "Nomor AFE": data_operational["afe_number"],
        "Tahun WP&B": data_operational["wpb_year"],
        "Tanggal Mulai": data_operational["start_date"],
        "Tanggal Selesai": data_operational["end_date"],
        "Total Budget": data_operational["total_budget"],
        "Nama Rig": data_operational["rig_name"],
        "Tipe Rig": data_operational["rig_type"],
        "RIG HP": data_operational["rig_horse_power"]
    }

    view_plan["technical"] = {
        "UWI": data_teknis["uwi"],
        "Nama Well": data_teknis["well_name"],
        "Alias Well": data_teknis["alias_long_name"],
        "Tipe Well": data_teknis["well_type"],
        "Tipe Profil Well": data_teknis["well_profile_type"],
        "Hidrokarbon Target": data_teknis["hydrocarbon_target"],
        "Tipe Lingkungan": data_teknis["environment_type"],
        "Longitude Permukaan": data_teknis["surface_longitude"],
        "Latitude Permukaan": data_teknis["surface_latitude"],
        "Longitude Bottom Hole": data_teknis["bottom_hole_longitude"],
        "Latitude Bottom Hole": data_teknis["bottom_hole_latitude"],
        "Maximum Inclination": data_teknis["maximum_inclination"],
        "Azimuth": data_teknis["azimuth"],
        "Nama Seismic Line": data_teknis["line_name"],
        "Tanggal Tajak": data_teknis["spud_date"],
        "Tanggal Selesai Drilling": data_teknis["final_drill_date"],
        "Tanggal Komplesi": data_teknis["completion_date"],
        "Elevasi Rotary Table": f'{data_teknis["rotary_table_elev"]} {data_teknis["rotary_table_elev_uom"]}',
        "Elevasi Kelly Bushing": f'{data_teknis["kb_elev"]} {data_teknis["kb_elev_uom"]}',
        "Elevasi Derrick Floor": f'{data_teknis["derrick_floor_elev"]} {data_teknis["derrick_floor_elev_uom"]}',
        "Elevasi Ground": f'{data_teknis["ground_elev"]} {data_teknis["ground_elev_uom"]}',
        "Mean Sea Level": f'{data_teknis["mean_sea_level"]} {data_teknis["mean_sea_level_uom"]}',
        "Kick Off Point": f'{data_teknis["kick_off_point"]} {data_teknis["kick_off_point_uom"]} from {data_teknis["depth_datum"]}',
        "Maximum TVD": f'{data_teknis["maximum_tvd"]} {data_teknis["maximum_tvd_uom"]} from {data_teknis["depth_datum"]}',
        "Final MD": f'{data_teknis["final_md"]} {data_teknis["final_md_uom"]} from {data_teknis["depth_datum"]}',
    }
    
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
    
    view_plan['operational']['work_breakdown_structure'] = wbs
    
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
    
    
