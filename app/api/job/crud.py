from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.job.models import *
from app.api.job.schemas import *
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

def operate_job(id: str, db: Session, user):
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
    db_job.actual_job = job_schema_map[db_job.job_type]['model']['actual'](**parse_schema(job_actual_temporary_schema))
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

def create_daily_operations_report(db: Session, report: DailyOperationsReportCreate):
    db_report = DailyOperationsReport(**report.dict(exclude={'time_breakdowns', 'personnel', 'Incidents', 'bit_records','bottom_hole_assemblies','drilling_fluids','mud_additives','bulk_materials','directional_surveys','pumps','weather'}))
    
    for tb in report.time_breakdowns:
        start_datetime = datetime.combine(report.report_date, tb.start_time)
        end_datetime = datetime.combine(report.report_date, tb.end_time)
        
        # If end_time is earlier than start_time, assume it's the next day
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)
        
        db_time_breakdown = TimeBreakdown(
            daily_operations_report_id=db_report.id,
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
            daily_operations_report_id=db_report.id,
            company=p.company,
            people=p.people
        )
        db_report.personnel.append(db_personnel)
    
    for incident in report.Incidents:
        db_incident = Incident(
            daily_operations_report_id=db_report.id,
            incidents_time=incident.incidents_time,
            incident=incident.incident,
            incident_type=incident.incident_type,
            comments=incident.comments
        )
        db_report.Incidents.append(db_incident)
    for br_data in report.bit_records:
        db_bit_record = BitRecord(
            daily_operations_report_id=db_report.id,
            bit_number=br_data.bit_number,
            bit_run=br_data.bit_run,
            bit_size=br_data.bit_size,
            manufacturer=br_data.manufacturer,
            iadc_code=br_data.iadc_code,
            jets=br_data.jets,
            serial=br_data.serial,
            depth_out=br_data.depth_out,
            depth_in=br_data.depth_in,
            meterage=br_data.meterage,
            bit_hours=br_data.bit_hours,
            nozzels=br_data.nozzels,
            dull_grade=br_data.dull_grade
        )
        db_report.bit_records.append(db_bit_record)

    for bha_data in report.bottom_hole_assemblies:
        db_bha = BottomHoleAssembly(
            daily_operations_report_id=db_report.id,
            bha_number=bha_data.bha_number,
            bha_run=bha_data.bha_run
        )
        for component_data in bha_data.components:
            db_component = BHAComponent(
                component=component_data.component,
                outer_diameter=component_data.outer_diameter,
                length=component_data.length
            )
            db_bha.components.append(db_component)
        db_report.bottom_hole_assemblies.append(db_bha)

    for drilling_fluid in report.drilling_fluids:
        db_drilling_fluid = DrillingFluid(  # Assuming you're using UUID
            daily_operations_report_id=db_report.id,  # Link to the current report
            mud_type=drilling_fluid.mud_type,
            time=drilling_fluid.time,
            mw_in=drilling_fluid.mw_in,
            mw_out=drilling_fluid.mw_out,
            temp_in=drilling_fluid.temp_in,
            temp_out=drilling_fluid.temp_out,
            pres_grad=drilling_fluid.pres_grad,
            visc=drilling_fluid.visc,
            pv=drilling_fluid.pv,
            yp=drilling_fluid.yp,
            gels_10_sec=drilling_fluid.gels_10_sec,
            gels_10_min=drilling_fluid.gels_10_min,
            fluid_loss=drilling_fluid.fluid_loss,
            ph=drilling_fluid.ph,
            solids=drilling_fluid.solids,
            sand=drilling_fluid.sand,
            water=drilling_fluid.water,
            oil=drilling_fluid.oil,
            hgs=drilling_fluid.hgs,
            lgs=drilling_fluid.lgs,
            ltlp=drilling_fluid.ltlp,
            hthp=drilling_fluid.hthp,
            cake=drilling_fluid.cake,
            e_stb=drilling_fluid.e_stb,
            pf=drilling_fluid.pf,
            mf=drilling_fluid.mf,
            pm=drilling_fluid.pm,
            ecd=drilling_fluid.ecd
        )
        db_report.drilling_fluids.append(db_drilling_fluid)

    for mud_additive in report.mud_additives:
        db_mud_additive = MudAdditive(
            daily_operations_report_id=db_report.id,
            mud_additive_type=mud_additive.mud_additive_type,
            amount=mud_additive.amount
        )
        db_report.mud_additives.append(db_mud_additive)

    for bulk_material in report.bulk_materials:
        db_bulk_material = BulkMaterial(
            id=str(uuid4()),
            daily_operations_report_id=db_report.id,
            material_type=bulk_material.material_type,
            material_name=bulk_material.material_name,
            material_uom=bulk_material.material_uom,
            received=bulk_material.received,
            consumed=bulk_material.consumed,
            returned=bulk_material.returned,
            adjust=bulk_material.adjust,
            ending=bulk_material.ending
        )
        db_report.bulk_materials.append(db_bulk_material)

    for directional_survey in report.directional_surveys:
        db_directional_survey = DirectionalSurvey(
            daily_operations_report_id=db_report.id,
            measured_depth=directional_survey.measured_depth,
            azimuth=directional_survey.azimuth,
            inclination=directional_survey.inclination
        )
        db_report.directional_surveys.append(db_directional_survey)
    for pump in report.pumps:
        db_pump = Pumps(
            daily_operations_report_id=db_report.id,
            slow_speed=pump.slow_speed,
            circulate=pump.circulate,
            strokes=pump.strokes,
            pressure=pump.pressure,
            liner_size=pump.liner_size,
            efficiency=pump.efficiency 
        )
        db_report.pumps.append(db_pump)

    db_weather = Weather(
        daily_operations_report_id=db_report.id,
        temperature_high=report.weather.temperature_high,
        temperature_low=report.weather.temperature_low,
        wind_direction=report.weather.wind_direction,
        wind_speed=report.weather.wind_speed,
        chill_factor=report.weather.chill_factor,
        wave_height=report.weather.wave_height,
        wave_current_speed=report.weather.wave_current_speed,
        road_condition=report.weather.road_condition,
        visibility=report.weather.visibility,
        barometric_pressure=report.weather.barometric_pressure
    )
    db_report.weather = db_weather
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return create_api_response(
        success=True,
        message="Daily Operations Report created successfully",
    )

def update_actual_exploration(
    db: Session, 
    exploration_id: str, 
    exploration_update: ActualExplorationUpdate) -> ActualExploration:
    db_exploration = db.query(ActualExploration).filter(ActualExploration.id == exploration_id).first()
    if not db_exploration:
        return None
    
    update_data = exploration_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exploration, key, value)
    
    db.add(db_exploration)
    db.commit()
    db.refresh(db_exploration)
    return db_exploration

def create_job_issue(db: Session, job_issue: JobIssueCreate) -> JobIssue:
    db_job_issue = JobIssue(
        job_id=job_issue.job_id,
        date_time=job_issue.date_time,
        severity=job_issue.severity,
        description=job_issue.description,
        resolved=job_issue.resolved,
        resolved_date_time=job_issue.resolved_date_time
    )
    db.add(db_job_issue)
    db.commit()
    db.refresh(db_job_issue)
    return db_job_issue

def update_job_issue(db: Session, job_issue_id: str, job_issue_update: JobIssueUpdate) -> Optional[JobIssue]:
    db_job_issue = db.query(JobIssue).filter(JobIssue.id == job_issue_id).first()
    if db_job_issue is None:
        return None
    
    update_data = job_issue_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job_issue, key, value)
    
    db.add(db_job_issue)
    db.commit()
    db.refresh(db_job_issue)
    return db_job_issue

def get_wrm_data_by_job_id(
    db: Session, 
    actual_job_id: str, 
    model: Type[Union[ActualExploration, ActualDevelopment, ActualWorkover, ActualWellService]]
) -> Optional[Union[ActualExplorationUpdate, ActualDevelopmentUpdate, ActualWorkoverUpdate, ActualWellServiceUpdate]]:
    # Query untuk mendapatkan data WRM berdasarkan model yang diberikan
    wrm_data = db.query(model).filter(model.id == actual_job_id).first()

    if wrm_data is None:
        return None

    # Menentukan jenis Update berdasarkan model
    if model == ActualExploration:
        return ActualExplorationUpdate(
            wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
            wrm_ippkh=wrm_data.wrm_ippkh,
            wrm_ukl_upl=wrm_data.wrm_ukl_upl,
            wrm_amdal=wrm_data.wrm_amdal,
            wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
            wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
            wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
            wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
            wrm_internal_kkks=wrm_data.wrm_internal_kkks,
            wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
        )
    elif model == ActualDevelopment:
        return ActualDevelopmentUpdate(
            wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
            wrm_ippkh=wrm_data.wrm_ippkh,
            wrm_ukl_upl=wrm_data.wrm_ukl_upl,
            wrm_amdal=wrm_data.wrm_amdal,
            wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
            wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
            wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
            wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
            wrm_internal_kkks=wrm_data.wrm_internal_kkks,
            wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
        )
    elif model == ActualWorkover:
        return ActualWorkoverUpdate(
           wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
            wrm_ippkh=wrm_data.wrm_ippkh,
            wrm_ukl_upl=wrm_data.wrm_ukl_upl,
            wrm_amdal=wrm_data.wrm_amdal,
            wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
            wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
            wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
            wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
            wrm_internal_kkks=wrm_data.wrm_internal_kkks,
            wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
        )
    elif model == ActualWellService:
        return ActualWellServiceUpdate(
            wrm_pembebasan_lahan=wrm_data.wrm_pembebasan_lahan,
            wrm_ippkh=wrm_data.wrm_ippkh,
            wrm_ukl_upl=wrm_data.wrm_ukl_upl,
            wrm_amdal=wrm_data.wrm_amdal,
            wrm_pengadaan_rig=wrm_data.wrm_pengadaan_rig,
            wrm_pengadaan_drilling_services=wrm_data.wrm_pengadaan_drilling_services,
            wrm_pengadaan_lli=wrm_data.wrm_pengadaan_lli,
            wrm_persiapan_lokasi=wrm_data.wrm_persiapan_lokasi,
            wrm_internal_kkks=wrm_data.wrm_internal_kkks,
            wrm_evaluasi_subsurface=wrm_data.wrm_evaluasi_subsurface
        )
    else:
        raise ValueError("Unsupported model type")

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

def check_daily_operation_report(db: Session, job_instance_id: str, date: str) -> bool:
    """
    Check if a daily operation report exists for the given job instance and date.
    
    :param db: Database session
    :param job_instance_id: ID of the job instance
    :param date: Date to check
    :return: True if a report exists, False otherwise
    """
    return db.query(DailyOperationsReport)\
        .join(Job, and_(Job.id == DailyOperationsReport.job_id, Job.job_plan_id == job_instance_id))\
        .filter(DailyOperationsReport.report_date == date)\
        .first() is not None

def get_date_color(db: Session, job_instance_id: str, check_date: date) -> str:
    """
    Determine the color for a given date based on the specified conditions.
    
    :param db: Database session
    :param job_instance_id: ID of the job instance
    :param check_date: Date to check
    :return: Color string ('white', 'red', or 'green')
    """
    today = date.today()
    
    if check_date > today:
        return "gray"
    elif check_date < today:
        if check_daily_operation_report(db, job_instance_id, check_date.strftime('%Y-%m-%d')):
            return "green"
        else:
            return "red"
    else:  # check_date == today
        if check_daily_operation_report(db, job_instance_id, check_date.strftime('%Y-%m-%d')):
            return "green"
        else:
            return "white"

