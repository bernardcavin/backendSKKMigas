from xml.dom import ValidationErr
from xml.dom.minidom import Document
from fastapi.exceptions import HTTPException
from pyparsing import C
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.job.models import *
from app.api.job.schemas import job
from app.api.well.models import ActualWell
from app.core.schema_operations import create_api_response, parse_schema
from app.api.job.utils import *
from app.api.visualize.schemas import VisualizeCasing
from app.api.visualize.routes import request_visualize_casing
from well_profile import load
import pandas as pd
from typing import Union,Type
from sqlalchemy.sql import and_
from pydantic import ValidationError
import io
from uuid import uuid4

def create_job_plan(db: Session, job_type: JobType, plan: object, user):
    db_job = Job(**parse_schema(plan))
    db_job.kkks_id = user.kkks_id
    db_job.job_type = job_type
    db_job.date_proposed = datetime.now().date()
    db_job.planning_status = PlanningStatus.PROPOSED
    db_job.created_by_id = user.id
    db_job.time_created = datetime.now()
    if isinstance(plan, (CreateExplorationJob, CreateDevelopmentJob)):
        db_job.job_plan.well.area_id = plan.area_id
        db_job.job_plan.well.field_id = plan.field_id
        db_job.job_plan.well.kkks_id = user.kkks_id
    db.add(db_job)
    db.commit()
    return db_job.id

def map_to_schema(schema, row):
    data = {}
    for field, field_type in schema.__fields__.items():
        if hasattr(field_type.type_, '__fields__'):  # If it's a nested model
            nested_data = {k.replace(f'{field}_', ''): v for k, v in row.items() if k.startswith(f'{field}_')}
            data[field] = map_to_schema(field_type.type_, nested_data)
        else:
            data[field] = row.get(field)
    return schema(**data)

def upload_batch(db: Session, content: bytes, job_type: JobType, user):

    error_list = []
    validated_data = []
    
    dtype_map = job_schema_map[job_type]['upload_headers']['plan']

    try:
        df = pd.read_excel(io.BytesIO(content), skiprows=1,
            converters=dtype_map
        )

        # Check if all required columns are present
        required_columns = set(dtype_map.keys())
        missing_columns = required_columns - set(df.columns)
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Rename the columns based on the provided dictionary
        df.rename(columns=plan_label_key_mapping, inplace=True)
        
        df = df.replace({float('nan'): None})
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    area_names = db.query(Area.name).all()
    field_names = db.query(Lapangan.name).all()

    for index, row in df.iterrows():
        
        try:
            
            if row['area_name'] not in [area.name for area in area_names]:
                raise AreaDoesntExist

            if row['field_name'] not in [field.name for field in field_names]:
                raise FieldDoesntExist
            
            if job_type in [JobType.WORKOVER,JobType.WELLSERVICE]:
                if row.get('well_name',None):
                    well = db.query(ActualWell).filter(ActualWell.well_name == row['well_name']).first()
                    if well is None:
                        row['well_id'] = 'not found'
                        raise WellDoesntExist
                    else:
                        row['well_id'] = well.id
                        
            row['area_id'] = db.query(Area).filter(Area.name == row['area_name']).first().id
            row['field_id'] = db.query(Lapangan).filter(Lapangan.name == row['field_name']).first().id
            
        except AreaDoesntExist:
            error_list.append(f'Row {index + 2} in Area: Invalid area name')
            
        except FieldDoesntExist:
            error_list.append(f'Row {index + 2} in Field: Invalid field name')
            
        except WellDoesntExist:
            error_list.append(f'Row {index + 2} in Well: Invalid well name')
        
        try:
            
            job_schema = job_schema_map[job_type]['job']
            job_plan_schema = job_schema_map[job_type]['schema']['plan']

            data_dict = {
                "area_id": row.get('area_id','not found'),
                "field_id": row.get('field_id','not found'),
                "contract_type": row['contract_type'],
                "afe_number": row['afe_number'],
                "wpb_year": row['wpb_year'],                
                "job_plan": {
                    **build_nested_model(job_plan_schema, row.to_dict())
                }
            }
            
            plan = job_schema(**data_dict)
            
            db_job = Job(**parse_schema(plan))
            db_job.kkks_id = user.kkks_id
            db_job.job_type = JobType.EXPLORATION
            db_job.date_proposed = datetime.now().date()
            db_job.planning_status = PlanningStatus.PROPOSED
            db_job.created_by_id = user.id
            db_job.time_created = datetime.now()
            
            if isinstance(plan, (CreateExplorationJob, CreateDevelopmentJob)):
                db_job.job_plan.well.area_id = plan.area_id
                db_job.job_plan.well.field_id = plan.field_id
                db_job.job_plan.well.kkks_id = user.kkks_id
            
            validated_data.append(db_job)
            
        except ValidationError as e:
            
            for error in e.errors():
                
                error_list.append(f'Row {index + 2} in {plan_key_label_mapping.get(error["loc"][-1], error["loc"][-1])}: {error["msg"]}. Your input was {error['input']}')
            
    if error_list:
        raise HTTPException(status_code=400, detail={"errors": error_list})
    
    db.add_all(validated_data)
    db.commit()
    
    return {"message": "Data uploaded successfully", "validated_data": validated_data} 

def update_job_plan(db: Session, job_id: str, plan: object, user):
    db_job = db.query(Job).filter_by(id=job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job plan not found")
    if db_job.planning_status == PlanningStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Job is already approved")

    db_job_new = Job(**parse_schema(plan))
    db_job_new.id = job_id
    db_job_new.kkks_id = db_job.kkks_id
    db_job_new.job_type = db_job.job_type
    db_job_new.date_proposed = db_job.date_proposed
    db_job_new.planning_status = PlanningStatus.PROPOSED
    db_job_new.created_by_id = db_job.created_by_id
    db_job_new.time_created = db_job.time_created
    db_job_new.last_edited_by_id = user.id
    db_job_new.last_edited = datetime.now().date()

    db.delete(db_job)
    db.add(db_job_new)
    db.commit()
    return db_job_new

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

def operate_job(id: str, db: Session, surat_tajak: SuratTajakSchema):
    db_job = db.query(Job).filter_by(id=id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.operation_status = OperationStatus.OPERATING
    db_job.date_started = datetime.now().date()
    
    actual_schema = job_schema_map[db_job.job_type]['schema']['actual']
    plan_schema = job_schema_map[db_job.job_type]['schema']['plan']
    
    if db_job.job_type in [JobType.EXPLORATION, JobType.DEVELOPMENT]:
        
        job_plan_schema = plan_schema.model_validate(db_job.job_plan, from_attributes=True)
        
        job_plan_dict = {
            **job_plan_schema.model_dump(
                include={
                    'start_date':True,
                    'end_date':True,
                    'total_budget':True,
                    'job_operation_days':True,
                    'rig_name':True,
                    'rig_type':True,
                    'rig_horse_power':True,
                    'well' : {
                        'unit_type',
                        'uwi',
                        'area_id',
                        'field_id',
                        'well_name',
                        'alias_long_name',
                        'well_type',
                        'well_profile_type',
                        'well_directional_type',
                        'hydrocarbon_target',
                        'environment_type',
                        'surface_longitude',
                        'surface_latitude',
                        'bottom_hole_longitude',
                        'bottom_hole_latitude',
                        'maximum_inclination',
                        'azimuth',
                        'line_name',
                        'spud_date',
                        'final_drill_date',
                        'completion_date',
                        'rotary_table_elev',
                        'kb_elev',
                        'derrick_floor_elev',
                        'ground_elev',
                        'mean_sea_level',
                        'depth_datum',
                        'kick_off_point',
                        'maximum_tvd',
                        'final_md',
                        'remark',
                    }
                }
            )
        }
        
        job_plan_dict['well']['area_id'] = db_job.job_plan.well.area_id
        job_plan_dict['well']['field_id'] = db_job.job_plan.well.field_id
        job_plan_dict['well']['kkks_id'] = db_job.job_plan.well.kkks_id
        
        job_actual_temporary_schema = actual_schema(**job_plan_dict)
        
    else:
        job_actual_temporary_schema = actual_schema(**plan_schema.model_validate(db_job.job_plan, from_attributes=True).model_dump(
            exclude={
                'job_hazards':True,
                'job_documents':True,
                'work_breakdown_structure':True,
            }
        ))
        
    actual_job_id = str(uuid4())
    
    db_job.actual_job = job_schema_map[db_job.job_type]['model']['actual'](**parse_schema(job_actual_temporary_schema), id=actual_job_id)
    
    #surat_tajak
    db_surat_tajak_document = JobDocument(
        job_instance_id = actual_job_id,
        file_id=surat_tajak.file_id,
        document_type=JobDocumentType.SURAT_TAJAK
    )
    db.add(db_surat_tajak_document)
    db.commit()
    return {"message": "Job operation started successfully"}

def get_job_plan(id: str, db: Session) -> dict:
    db_job = db.query(Job).get(id)
    print('test')
    print(db_job)
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

    job_wbs = db_plan.work_breakdown_structure.events
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

def time_to_string(t: time) -> str:
    return t.strftime('%H:%M:%S')

def string_to_time(s: str) -> time:
    return datetime.strptime(s, '%H:%M:%S').time()

# def parse_schema(obj):
#     parsed_dict = {}
#     for k, v in obj.__dict__.items():
#         if not k.startswith('_'):
#             if isinstance(v, time):
#                 parsed_dict[k] = time_to_string(v)
#             else:
#                 parsed_dict[k] = v
#     return parsed_dict

def create_daily_operations_report(db: Session, job_id: str, report: DailyOperationsReportCreate):
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    existing_dor = db.query(DailyOperationsReport).filter(DailyOperationsReport.job_id == job_id, DailyOperationsReport.report_date == report.report_date).first()
    if existing_dor:
        raise HTTPException(status_code=400, detail="Daily Operations Report already exists")
    
    db_report = DailyOperationsReport(
        **parse_schema(report), job_id = job_id
    )
    
    db.add(db_report)
    db.commit()

def edit_daily_operations_report(db: Session, job_id: str, report_date: date, report: DailyOperationsReportEdit):
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    old_report = db.query(DailyOperationsReport).filter(DailyOperationsReport.job_id == job_id, DailyOperationsReport.report_date == report_date).first()
    
    new_report = DailyOperationsReport(
        **parse_schema(report), job_id = job_id, report_date = old_report.report_date, id = old_report.id
    )
    db.delete(old_report)

    db.commit()

# def update_actual_exploration(
#     db: Session, 
#     exploration_id: str, 
#     exploration_update: ActualExplorationUpdate) -> ActualExploration:
#     db_exploration = db.query(ActualExploration).filter(ActualExploration.id == exploration_id).first()
#     if not db_exploration:
#         return None
    
#     update_data = exploration_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_exploration, key, value)
    
#     db.add(db_exploration)
#     db.commit()
#     db.refresh(db_exploration)
#     return db_exploration


#job issues
def get_job_issues(db: Session, job_id: str) -> List[JobIssue]:
    return db.query(JobIssue).filter(JobIssue.job_id == job_id).all()

def create_job_issue(db: Session, job_id: str, job_issue: JobIssueCreate) -> JobIssue:
    db_job_issue = JobIssue(
        **parse_schema(job_issue), job_id = job_id
    )
    db.add(db_job_issue)
    db.commit()

def edit_job_issue(db: Session, job_issue_id: str, job_issue_update: JobIssueEdit) -> Optional[JobIssue]:
    db_job_issue = db.query(JobIssue).filter(JobIssue.id == job_issue_id).first()
    if db_job_issue is None:
        return None
    
    update_data = job_issue_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job_issue, key, value)
    
    db.add(db_job_issue)
    db.commit()

def delete_job_issue(db: Session, job_issue_id: str) -> Optional[JobIssue]:
    db_job_issue = db.query(JobIssue).filter(JobIssue.id == job_issue_id).first()
    if db_job_issue is None:
        raise HTTPException(status_code=404, detail="Job issue not found")
    db.delete(db_job_issue)
    db.commit()

def resolve_job_issue(db: Session, job_issue_id: str) -> Optional[JobIssue]:
    db_job_issue = db.query(JobIssue).filter(JobIssue.id == job_issue_id).first()
    if db_job_issue is None:
        raise HTTPException(status_code=404, detail="Job issue not found")
    db_job_issue.resolved = True
    db_job_issue.resolved_date_time = datetime.now()
    db.commit()

def get_wrm_requirements(
    db: Session, 
    job_id: str
):
    job = db.query(Job).filter(Job.id == job_id).first()
    job_plan = job.job_plan
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    output = {}

    for wrm in list(job_schema_map[job.job_type]['wrm'].model_fields.keys()):
        output[wrm] = getattr(job_plan, wrm)
    
    return output

def get_wrm_progress(
    db: Session, 
    job_id: str
):
    job = db.query(Job).filter(Job.id == job_id).first()
    job_plan = job.job_plan
    actual_job = job.actual_job
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    output = {}

    for wrm in list(job_schema_map[job.job_type]['wrm'].model_fields.keys()):
        if getattr(job_plan, wrm):
            output[wrm] = getattr(actual_job, wrm)
    
    return output
                
def update_wrm(
    db: Session, 
    job_id: str, 
    wrm_data: object
):
    job = db.query(Job).filter(Job.id == job_id).first()
    job_actual = job.job_plan
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    for wrm in list(job_schema_map[job.job_type]['wrm'].model_fields.keys()):
        setattr(job_actual, wrm, wrm_data.get(wrm))
    
    db.commit()


# def get_wrm_data_by_job_id(
#     db: Session, 
#     actual_job_id: str, 
#     model: Type[Union[ActualExploration, ActualDevelopment, ActualWorkover, ActualWellService]]
# ) -> Optional[Union[ActualExplorationUpdate, ActualDevelopmentUpdate, ActualWorkoverUpdate, ActualWellServiceUpdate]]:
#     # Query untuk mendapatkan data WRM berdasarkan model yang diberikan
#     wrm_data = db.query(model).filter(model.id == actual_job_id).first()

#     if wrm_data is None:
#         return None

#     # Menentukan jenis Update berdasarkan model
#     if model == ActualExploration:
#         return ActualExplorationUpdate(
#             wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
#             wrm_ippkh=wrm_data.wrm_ippkh,
#             wrm_ukl_upl=wrm_data.wrm_ukl_upl,
#             wrm_amdal=wrm_data.wrm_amdal,
#             wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
#             wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
#             wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
#             wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
#             wrm_internal_kkks=wrm_data.wrm_internal_kkks,
#             wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
#         )
#     elif model == ActualDevelopment:
#         return ActualDevelopmentUpdate(
#             wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
#             wrm_ippkh=wrm_data.wrm_ippkh,
#             wrm_ukl_upl=wrm_data.wrm_ukl_upl,
#             wrm_amdal=wrm_data.wrm_amdal,
#             wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
#             wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
#             wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
#             wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
#             wrm_internal_kkks=wrm_data.wrm_internal_kkks,
#             wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
#         )
#     elif model == ActualWorkover:
#         return ActualWorkoverUpdate(
#            wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
#             wrm_ippkh=wrm_data.wrm_ippkh,
#             wrm_ukl_upl=wrm_data.wrm_ukl_upl,
#             wrm_amdal=wrm_data.wrm_amdal,
#             wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
#             wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
#             wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
#             wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
#             wrm_internal_kkks=wrm_data.wrm_internal_kkks,
#             wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
#         )
#     elif model == ActualWellService:
#         return ActualWellServiceUpdate(
#             wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
#             wrm_ippkh=wrm_data.wrm_ippkh,
#             wrm_ukl_upl=wrm_data.wrm_ukl_upl,
#             wrm_amdal=wrm_data.wrm_amdal,
#             wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
#             wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
#             wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
#             wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
#             wrm_internal_kkks=wrm_data.wrm_internal_kkks,
#             wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
#         )
#     else:
#         raise ValueError("Unsupported model type")

def get_dor_dates(db: Session, job_id: str):
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    dor_dates = [date for (date,) in db.query(DailyOperationsReport.report_date).filter(DailyOperationsReport.job_id == job_id).all()]
    
    colored_dates = []

    actual_start_date = job.actual_start_date if job.actual_start_date is not None else job.plan_start_date
    actual_end_date = job.actual_end_date if job.actual_end_date is not None else job.plan_end_date
    
    # print(dor_dates)
    
    for _date in daterange(actual_start_date, actual_end_date):
        # if actual_start_date >= _date >= actual_end_date:
        if _date in dor_dates:
            color = 'green'
        elif _date == date.today():
            color = 'blue'
        else:
            color = 'gray'
        colored_dates.append(
            ColoredDate(
                date=_date,
                color=color
            )
        )
    
    return colored_dates

def get_dor_by_date(db: Session, job_id: str, dor_date: date):
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    dor = db.query(DailyOperationsReport).filter(DailyOperationsReport.report_date == dor_date).first()
    
    return dor

def get_wrmissues_data_by_job_id(db: Session, job_id: str) -> List[JobIssueResponse]:
    wrm_data = db.query(JobIssue).filter(JobIssue.job_id == job_id).all()
    return wrm_data

def get_drilling_operation(value: str) -> DrillingOperation:
    for operation in DrillingOperation:
        if value.lower() in operation.value.lower():
            return operation
    raise ValueError(f"No matching DrillingOperation found for: {value}")

def get_BHA(value: str) -> BHAComponentType:
    for bhacomponent in BHAComponentType:
        if value.lower() in bhacomponent.value.lower():
            return bhacomponent
    raise ValueError(f"No matching DrillingOperation found for: {value}")

def get_job_instance(db: Session, job_instance_id: str):
    return db.query(JobInstance).filter(JobInstance.job_instance_id == job_instance_id).first()

def get_job_operation_validations(db: Session, job_id: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_actual = job.actual_job
    
    error_list = check_fields(
        job_schema_map[job.job_type]['validation'].model_validate(job_actual)
    )
    
    return error_list

def finish_operation(
    db: Session, 
    job_id: str, 
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.operation_status = OperationStatus.FINISHED
    db_job.date_finished = datetime.now().date()
    db.commit()
    

def update_operation(
    db: Session, 
    job_id: str, 
    actual: Union[CreateActualExploration, CreateActualDevelopment, CreateActualWorkover, CreateActualWellService]
):
    db_job = db.query(Job).filter(Job.id ==job_id).first()
    db_job_actual_old = db_job.actual_job
    
    #find job_type
    actual_job_schema = job_schema_map[db_job.job_type]['schema']['actual']
    db_job_actual_new = actual_job_schema(**parse_schema(actual))
    
    #id
    db_job_actual_new.id = db_job_actual_old.id
    
    #wrm
    for wrm in list(job_schema_map[job.job_type]['wrm'].model_fields.keys()):
        setattr(db_job_actual_new, wrm, getattr(db_job_actual_old, wrm))
    
    db.delete(db_job_actual_old)
    db.add(db_job_actual_new)

    db.commit()

def propose_ppp(db: Session, job_id: str, ppp: ProposePPP):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    propose_ppp_model_fields = ProposePPP.model_fields().keys()
    
    syarat_ppp_fields = [x for x in propose_ppp_model_fields if x not in ["dokumen_lainnya"]]
    
    for syarat_ppp in syarat_ppp_fields:
        
        dokumen_syarat_obj = JobDocument(**getattr(ppp, syarat_ppp).model_dump(), job_instance_id = job.actual_job_id)
        
        setattr(job, syarat_ppp, dokumen_syarat_obj)
    
    documents = []
    
    for dokumen in ppp.dokumen_lainnya:
        documents.append(
            JobDocument(
                **dokumen.model_dump()
            )
        )
    
    db.add_all(documents)
    
    job.date_ppp_proposed = date.today()
    
    db.commit()

def approve_ppp(db: Session, job_id: str, approval: ApprovePPP):
    
    job = db.query(Job).filter(Job.id == job_id).first()
    
    approve_ppp_model_fields = ApprovePPP.model_fields().keys()
    
    for syarat_ppp in approve_ppp_model_fields:
        
        setattr(job, syarat_ppp, getattr(approval, syarat_ppp))
    
    db.commit()
    
    
    
    






