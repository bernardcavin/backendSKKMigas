from app.api.auth.models import KKKS, User, Role, Admin, KKKSUser
from app.api.auth.crud import pwd_context 
from app.api.spatial import models as spatial_models
from datetime import datetime, timedelta
from app.api.job import crud as job_crud
from app.api.job.schemas import *
from app.api.job.models import *
from app.api.well.schemas import *
from app.api.utils import models as utils_models
from app.api.spatial.models import *
import pandas as pd
import uuid
import random

from app.api.well.models import *

def default(o):
    if isinstance(o, (datetime)):
        return o.isoformat()

def random_enum_value(enum_class):
    enum_values = list(enum_class)
    return random.choice(enum_values)

def random_datetime_within_year(year: int) -> datetime:
    # Define the start of the year and the end of the year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    
    # Calculate the number of days between the start and end dates
    num_days = (end_date - start_date).days
    
    # Generate a random number of days and seconds
    random_days = random.randint(0, num_days - 1)
    random_seconds = random.randint(0, 86399)  # Total seconds in a day (24 * 60 * 60)
    
    # Create the random datetime
    random_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    
    return random_date

def generate_dummy_data(db, n: int):

    df_plan = pd.read_excel('app/scripts/dummy_data/Operation Days.xlsx', sheet_name='Plan')
    # df_actual = pd.read_excel('Operation Days.xlsx', sheet_name='Actual')
    
    plan_job_operation_days = []
    
    for i, row in df_plan.iterrows():
        plan_job_operation_days.append(
            {
                "unit_type": "Metrics",
                "phase": row['Event'],
                "depth_datum": "KB",
                "depth_in": row['Start Depth'],
                "depth_out": row['End Depth'],
                "operation_days": row['Days']
            }
        )
    
    # actual_job_operation_days = []
    
    # for i, row in df_actual.iterrows():
    #     actual_job_operation_days.append(
    #         {
    #             "phase": row['Event'],
    #             "depth_datum": "KB",
    #             "depth_in": row['Start Depth'],
    #             "depth_out": row['End Depth'],
    #             "depth_uom": "FEET",
    #             "operation_days": row['Days']
    #         }
    #     )
    
    wbs = pd.read_excel('app/scripts/dummy_data/wbs.xlsx')
    
    plan_wbs = []
    
    for i, row in wbs.iterrows():
        plan_wbs.append(
            {
                "event": row["Event"],
                "start_date": row["Start Date"].date(),
                "end_date": row["End Date"].date(),
                "remarks": "Nothing"
            }
        )
    
    casing = pd.read_excel('app/scripts/dummy_data/casing.xlsx')
        
    plan_casing = []
    
    for i, row in casing.iterrows():
        plan_casing.append(
            {
                "unit_type": "Metrics",
                "depth_datum": "RT",
                "depth": row["End Depth"],
                "length": row["End Depth"] - row["Start Depth"],
                "hole_diameter": 0,
                "casing_outer_diameter": row["Outer Diameter"],
                "casing_inner_diameter": row["Inner Diameter"],
                "casing_grade": '-',
                "casing_weight": row['Weight'],
                "connection": "string",
                "description": row['Casing Type']
            }
        )

    skk_user_id = str(uuid.uuid4())
    kkks_user_id = str(uuid.uuid4())
    
    db.add_all(
            [
                Admin(
                    id = skk_user_id,
                    username = f'skk',
                    email = f'skk@skk.com',
                    hashed_password = pwd_context.hash(f'skk'),
                    verified_status = True
                ),
                KKKSUser(
                    id = kkks_user_id,
                    username = f'kkks',
                    email = f'kkks@kkks.com',
                    hashed_password = pwd_context.hash(f'kkks'),
                    verified_status = True
                ),
                KKKSUser(
                    id = str(uuid.uuid4()),
                    username = f'kkks1',
                    email = f'kkks1@kkks.com',
                    hashed_password = pwd_context.hash(f'kkks1'),
                    verified_status = False
                )
            ]
        )

    i = n

    while i > 0:
        
        i -= 1

        kkks_id = str(uuid.uuid4())
        
        db.add(
            KKKS(
                id = kkks_id,
                name = f'KKKS0{i}'
            )
        )
        
        db.commit()

        area_id = str(uuid.uuid4())

        db.add(
            Area(
                id = area_id,
                kkks_id = kkks_id,
                label = f'AREA0{i}',
                name = f'AREA0{i}',
                phase = random_enum_value(AreaPhase),
                type = random_enum_value(AreaType),
                position = random_enum_value(AreaPosition),
                production_status = random_enum_value(AreaProductionStatus),
                region = random_enum_value(AreaRegion),
            )
        )

        db.commit()

        field_id = str(uuid.uuid4())

        db.add(
            spatial_models.Lapangan(
                id = field_id,
                name = f'FIELD0{i}',
                area_id = area_id,
            )
        )

        db.commit()

        db.add_all(
            [
                spatial_models.StratUnit(
                    area_id = area_id,
                    strat_unit_name = f'STRAT00{j}',
                    strat_type = random_enum_value(StratType),
                    strat_unit_type = random_enum_value(StratUnitType),
                    strat_petroleum_system =random_enum_value(PetroleumSystem),
                    remark = '-',
                ) for j in range(5)
            ]
        )

        db.commit()

        user_id = str(uuid.uuid4())

        user = KKKSUser(
                id = user_id,
                username = f'USER00{i}',
                email = f'email00{i}@email00{i}.com',
                hashed_password = pwd_context.hash(f'USER00{i}'),
                kkks_id = kkks_id,
                verified_status = True
            )

        db.add(
            user
        )
        
        db.commit()
        
        drilling_trajectory_file_id = str(uuid.uuid4())
        
        db.add_all(
            [
                utils_models.FileDB(
                    id =  drilling_trajectory_file_id,
                    filename = 'drilling_trajectory.xlsx',
                    size  = 10000,
                    content_type = 'xlsx',
                    upload_time = datetime.now(),
                    file_location = 'app/scripts/dummy_data/drilling_trajectory.xlsx',
                    uploaded_by_id = user_id,
                ),
            ]
        )
        
        db.commit()
        
        k = random.randint(0,10)
        
        i = i - k

        for j in range(k):

            plan_start = random_datetime_within_year(2024)

            contract_type = random_enum_value(ContractType).value
            
            job_type = random_enum_value(JobType)
            
            well_dict = {
                "unit_type": "Metrics",
                "uwi": f'{i+j}{j}',
                "field_id": field_id,
                "area_id": area_id,
                "kkks_id": kkks_id,
                "well_name": f'WELL0{i+j}{j}',
                "alias_long_name": "-",
                "well_type": random_enum_value(WellType).value,
                "well_status": random_enum_value(WellStatus).value,
                "well_profile_type": random_enum_value(WellProfileType).value,
                "well_directional_type": random_enum_value(WellDirectionalType).value,
                "hydrocarbon_target": random_enum_value(HydrocarbonTarget).value,
                "environment_type": random_enum_value(EnvironmentType).value,
                "surface_longitude": 106.816666,
                "surface_latitude": -6.200000,
                "bottom_hole_longitude": 106.816666,
                "bottom_hole_latitude": -6.200000,
                "maximum_inclination": 0,
                "azimuth": 0,
                "line_name": "string",
                "spud_date": "2024-08-31",
                "final_drill_date": "2024-08-31",
                "completion_date": "2024-08-31",
                "rotary_table_elev": 0,
                "kb_elev": 0,
                "derrick_floor_elev": 0,
                "ground_elev": 0,
                "mean_sea_level": 0,
                "depth_datum": "RT",
                "kick_off_point": 0,
                "maximum_tvd": 0,
                "final_md": 0,
                "remark": "string",
                "well_summary": [
                    {
                    "unit_type": "Metrics",
                    "depth_datum": "RT",
                    "depth": 0,
                    "hole_diameter": 0,
                    "bit": "string",
                    "casing_outer_diameter": 0,
                    "logging": "string",
                    "mud_program": "string",
                    "cementing_program": "string",
                    "bottom_hole_temperature": 0,
                    "rate_of_penetration": 0,
                    "remarks": "string"
                    }
                ],
                "well_test": [
                    {
                    "unit_type": "Metrics",
                    "depth_datum": "RT",
                    "zone_name": "string",
                    "zone_top_depth": 0,
                    "zone_bottom_depth": 0,
                    }
                ],
                "well_trajectory": 
                    {
                    "file_id": drilling_trajectory_file_id,
                    "data_format": DataFormat.PLAIN_TEXT,
                    }
                ,
                "well_casing": plan_casing,
            }
            
            plan_start_date = plan_start.date()
            plan_end_date = (plan_start+timedelta(days=20)).date()
            
            actual_start_date = (plan_start+timedelta(days=random.randint(0,5))).date()
            actual_end_date = (plan_start+timedelta(days=20+random.randint(0,5))).date()
            
            plan_total_budget = round(random.uniform(9999999, 999999),2)
            actual_total_budget = round(plan_total_budget*(1+random.uniform(-0.1, 0.1)),2)
            
            if job_type in [JobType.EXPLORATION, JobType.DEVELOPMENT]:
                
                rig_type = random_enum_value(RigType).value
                rig_hp = random.randint(100, 5000)
                
                plan_job_dict = {
                    "start_date": plan_start_date,
                    "end_date": plan_end_date,
                    "total_budget": plan_total_budget,
                    "rig_name": f'RIG0{j}',
                    "rig_type": rig_type,
                    "rig_horse_power": rig_hp,
                    "job_operation_days": plan_job_operation_days,
                    "work_breakdown_structure": plan_wbs,
                    "job_hazards": [
                    {
                        "hazard_type": "GAS KICK",
                        "hazard_description": "string",
                        "severity": "LOW",
                        "mitigation": "string",
                        "remark": "string"
                    }
                    ],
                    "well": well_dict,
                    "wrm_pembebasan_lahan": True,
                    "wrm_ippkh": True,
                    "wrm_ukl_upl": True,
                    "wrm_amdal": True,
                    "wrm_cutting_dumping": True,
                    "wrm_pengadaan_rig": True,
                    "wrm_pengadaan_drilling_services": True,
                    "wrm_pengadaan_lli": True,
                    "wrm_persiapan_lokasi": True,
                    "wrm_internal_kkks": True,
                    "wrm_evaluasi_subsurface": True
                }

                actual_job_dict = {
                    "start_date": actual_start_date,
                    "end_date": actual_end_date,
                    "total_budget": actual_total_budget,
                    "rig_name": f'RIG0{j}',
                    "rig_type": rig_type,
                    "rig_horse_power": rig_hp,
                    "job_operation_days": plan_job_operation_days,
                    "work_breakdown_structure": plan_wbs,
                    "job_hazards": [
                    {
                        "hazard_type": "GAS KICK",
                        "hazard_description": "string",
                        "severity": "LOW",
                        "mitigation": "string",
                        "remark": "string"
                    }
                    ],
                    "well": well_dict,
                    "wrm_pembebasan_lahan": random_enum_value(Percentage),
                    "wrm_ippkh": random_enum_value(Percentage),
                    "wrm_ukl_upl": random_enum_value(Percentage),
                    "wrm_amdal": random_enum_value(Percentage),
                    "wrm_cutting_dumping": random_enum_value(Percentage),
                    "wrm_pengadaan_rig": random_enum_value(Percentage),
                    "wrm_pengadaan_drilling_services": random_enum_value(Percentage),
                    "wrm_pengadaan_lli": random_enum_value(Percentage),
                    "wrm_persiapan_lokasi": random_enum_value(Percentage),
                    "wrm_internal_kkks": random_enum_value(Percentage),
                    "wrm_evaluasi_subsurface": random_enum_value(Percentage)
                }
                
                drilling_job_dict = {
                    "area_id": area_id,
                    "field_id": field_id,
                    "contract_type": contract_type,
                    "afe_number": f'AFE0{j}' if contract_type == 'COST-RECOVERY' else '-',
                    "wpb_year": 2024,
                    "job_plan": plan_job_dict,
                }
                
                if job_type == JobType.EXPLORATION:
                    work_schema = ExplorationJobPlan
                    job_plan_schema = CreateActualExploration
                    actual_work_schema = ActualExploration
                else:
                    work_schema = DevelopmentJobPlan
                    job_plan_schema = CreateActualDevelopment
                    actual_work_schema = ActualDevelopment
                    
                db_job = Job(
                    **job_crud.parse_schema(work_schema(**drilling_job_dict))
                )
                
                actual_job = actual_work_schema(
                    **job_crud.parse_schema(job_plan_schema(**actual_job_dict))
                )

            else:
                
                well_id = str(uuid.uuid4())
                
                plan_job_dict = {
                    "start_date": plan_start_date,
                    "end_date": plan_end_date,
                    "total_budget": plan_total_budget,
                    "job_operation_days": plan_job_operation_days,
                    "work_breakdown_structure": plan_wbs,
                    "job_hazards": [
                        {
                            "hazard_type": "GAS KICK",
                            "hazard_description": "string",
                            "severity": "LOW",
                            "mitigation": "string",
                            "remark": "string"
                        }
                        ],
                        "job_documents": [
                        {
                            "file_id": drilling_trajectory_file_id,
                            "document_type": "Drilling Plan",
                            "remark": "string"
                        }
                        ],
                        "equipment": "string",
                        "equipment_sepesifications": "string",
                        "well_id": well_id,
                        "job_category": random_enum_value(WOWSJobType).value,
                        "job_description": "string",
                        "onstream_oil": random.randint(0,50),
                        "onstream_gas": random.randint(0,50),
                        "onstream_water_cut": random.uniform(0.5,1),
                        "target_oil": random.randint(51,100),
                        "target_gas": random.randint(51,100),
                        "target_water_cut": random.uniform(0, 0.49)
                    }

                actual_job_dict = {
                    "start_date": actual_start_date,
                    "end_date": actual_end_date,
                    "total_budget": actual_total_budget,
                    "job_operation_days": plan_job_operation_days,
                    "work_breakdown_structure": plan_wbs,
                    "job_hazards": [
                    {
                        "hazard_type": "GAS KICK",
                        "hazard_description": "string",
                        "severity": "LOW",
                        "mitigation": "string",
                        "remark": "string"
                    }
                    ],
                    "job_documents": [
                    {
                        "file_id": drilling_trajectory_file_id,
                        "document_type": "Drilling Plan",
                        "remark": "string"
                    }
                    ],
                    "equipment": "string",
                    "equipment_sepesifications": "string",
                    "well_id": well_id,
                    "job_category": random_enum_value(WOWSJobType).value,
                    "job_description": "string",
                    "onstream_oil": random.randint(0,50),
                    "onstream_gas": random.randint(0,50),
                    "onstream_water_cut": random.uniform(0.5,1),
                    "target_oil": random.randint(51,100),
                    "target_gas": random.randint(51,100),
                    "target_water_cut": random.uniform(0, 0.49)
                    }

                
                wows_job_dict = {
                    "area_id": area_id,
                    "field_id": field_id,
                    "contract_type": contract_type,
                    "afe_number": f'AFE0{j}' if contract_type == 'COST-RECOVERY' else '-',
                    "wpb_year": 2024,
                    "job_plan": plan_job_dict,
                }
                        
                
                well_obj = ActualWell(
                    **job_crud.parse_schema(CreateActualWell(**well_dict)), well_instance_id=well_id
                )
                
                db.add(
                    well_obj
                )
                
                db.commit()
                
                if job_type == JobType.WORKOVER:
                    work_schema = WorkoverJobPlan
                    job_actual_schema = CreateActualWorkover
                    actual_work_schema = ActualWorkover
                else:
                    work_schema = WellServiceJobPlan
                    job_actual_schema = CreateActualWellService
                    actual_work_schema = ActualWellService
                    
                db_job = Job(
                    **job_crud.parse_schema(work_schema(**wows_job_dict))
                )
                
                actual_job = actual_work_schema(
                    **job_crud.parse_schema(job_actual_schema(**actual_job_dict))
                )

            db_job.kkks_id = kkks_id
            db_job.job_type = job_type
            db_job.date_proposed = datetime.now().date()
            db_job.planning_status = PlanningStatus.PROPOSED
            
            db_job.created_by_id = user_id
            db_job.time_created = datetime.now()
            
            random_approval_status = random.randint(0, 2)
            
            if random_approval_status == 1:
                db_job.planning_status = PlanningStatus.APPROVED
                db_job.date_approved = datetime.now().date()
                db_job.approved_by_id = user.id
                db_job.remarks = None
                
                random_operation_status = random.randint(0, 2)
                
                if random_operation_status == 1:
                    
                    db_job.operation_status = OperationStatus.OPERATING
                    db_job.date_started = (plan_start+timedelta(days=random.randint(0, 5))).date()
                    db_job.actual_job = actual_job
                
                elif random_operation_status == 2:
                    
                    db_job.operation_status = OperationStatus.FINISHED
                    db_job.date_started = (plan_start+timedelta(days=random.randint(0, 5))).date()
                    db_job.date_finished = (plan_start+timedelta(days=25)).date()
                    db_job.actual_job = actual_job

            elif random_approval_status == 2:
                db_job.planning_status = PlanningStatus.RETURNED
                db_job.date_returned = datetime.now().date()
                db_job.returned_by_id = user.id
                db_job.remarks = None

            db.add(db_job)
            
            db.commit()
