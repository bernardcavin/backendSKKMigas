from backend.routers.auth.models import KKKS, User, Role
from backend.routers.auth.crud import pwd_context
from backend.routers.spatial import models as spatial_models
from datetime import datetime, timedelta
from backend.routers.job import crud as job_crud
from backend.routers.job import models as job_models
from backend.routers.utils.routers import *
from backend.routers.utils import models as utils_models
from backend.database import SessionLocal
import os
import uuid
import random

import contextlib

from backend.routers.well.models import *


def default(o):
    if isinstance(o, (datetime)):
        return o.isoformat()

@contextlib.contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def generate_dummy_user():
        
    with get_db_context() as db:
        
        db.add_all(
                [
                    User(
                        id = str(uuid.uuid4()),
                        username = f'skk',
                        email = f'skk@skk.com',
                        hashed_password = pwd_context.hash(f'skk'),
                        role = Role.Admin,
                        verified_status = True
                    ),
                    User(
                        id = str(uuid.uuid4()),
                        username = f'kkks',
                        email = f'kkks@kkks.com',
                        hashed_password = pwd_context.hash(f'kkks'),
                        role = Role.KKKS,
                        verified_status = True
                    ),
                    User(
                        id = str(uuid.uuid4()),
                        username = f'kkks1',
                        email = f'kkks1@kkks.com',
                        hashed_password = pwd_context.hash(f'kkks1'),
                        role = Role.KKKS,
                        verified_status = True
                    )
                ]
            )
        
        db.commit()
    

def generate_dummy_data(n: int):
    
    
    df_plan = pd.read_excel('backend/utils/dummy_data/Operation Days.xlsx', sheet_name='Plan')
    # df_actual = pd.read_excel('Operation Days.xlsx', sheet_name='Actual')
    
    plan_job_operation_days = []
    
    for i, row in df_plan.iterrows():
        plan_job_operation_days.append(
            {
                "phase": row['Event'],
                "depth_datum": "KB",
                "depth_in": row['Start Depth'],
                "depth_out": row['End Depth'],
                "depth_uom": "FEET",
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
    
    wbs = pd.read_excel('backend/utils/dummy_data/wbs.xlsx')
    
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
    
    casing = pd.read_excel('backend/utils/dummy_data/casing.xlsx')
        
    plan_casing = []
    
    for i, row in casing.iterrows():
        plan_casing.append(
            {
                "depth_datum": "RT",
                "depth": row["End Depth"],
                "depth_uom": "FEET",
                "length": row["End Depth"] - row["Start Depth"],
                "length_uom": "FEET",
                "hole_diameter": 0,
                "hole_diameter_uom": "INCH",
                "casing_outer_diameter": row["Outer Diameter"],
                "casing_outer_diameter_uom": "INCH",
                "casing_inner_diameter": row["Inner Diameter"],
                "casing_inner_diameter_uom": "INCH",
                "casing_grade": '-',
                "casing_weight": row['Weight'],
                "casing_weight_uom": "PPF",
                "connection": "string",
                "description": row['Casing Type']
            }
        )
    
    
    with get_db_context() as db:
        
        db.add_all(
                [
                    User(
                        id = str(uuid.uuid4()),
                        username = f'skk',
                        email = f'skk@skk.com',
                        hashed_password = pwd_context.hash(f'skk'),
                        role = Role.Admin,
                        verified_status = True
                    ),
                    User(
                        id = str(uuid.uuid4()),
                        username = f'kkks',
                        email = f'kkks@kkks.com',
                        hashed_password = pwd_context.hash(f'kkks'),
                        role = Role.KKKS,
                        verified_status = True
                    ),
                    User(
                        id = str(uuid.uuid4()),
                        username = f'kkks1',
                        email = f'kkks1@kkks.com',
                        hashed_password = pwd_context.hash(f'kkks1'),
                        role = Role.KKKS,
                        verified_status = True
                    )
                ]
            )

        for i in range(n):

            kkks_id = str(uuid.uuid4())
            
            db.add(
                KKKS(
                    id = kkks_id,
                    nama_kkks = f'KKKS0{i}'
                )
            )

            area_id = str(uuid.uuid4())

            db.add(
                Area(
                    id = area_id,
                    kkks_id = kkks_id,
                    label = f'AREA0{i}',
                    area_name = f'AREA0{i}',
                    area_phase = random_enum_value(AreaPhase),
                    area_type = random_enum_value(AreaType),
                    area_position = random_enum_value(AreaPosition),
                    area_production_status = random_enum_value(AreaProductionStatus),
                    area_region = random_enum_value(AreaRegion),
                )
            )

            field_id = str(uuid.uuid4())

            db.add(
                spatial_models.Field(
                    id = field_id,
                    field_name = f'FIELD0{i}',
                    area_id = area_id,
                )
            )

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

            user_id = str(uuid.uuid4())

            user = User(
                    id = user_id,
                    username = f'USER00{i}',
                    email = f'email00{i}@email00{i}.com',
                    hashed_password = pwd_context.hash(f'USER00{i}'),
                    role = Role.KKKS,
                    kkks_id = kkks_id,
                    verified_status = True
                )

            db.add(
                user
            )
            
            drilling_trajectory_file_id = str(uuid.uuid4())
            
            db.add_all(
                [
                    utils_models.FileDB(
                        id =  drilling_trajectory_file_id,
                        filename = 'drilling_trajectory.xlsx',
                        size  = 10000,
                        content_type = 'xlsx',
                        upload_time = datetime.now(),
                        file_location = 'backend/utils/dummy_data/drilling_trajectory.xlsx',
                        uploaded_by_id = user_id,
                    ),
                ]
            )
            

            for j in range(random.randint(0,5)):

                plan_start = random_datetime_within_year(2024)

                contract_type = random_enum_value(ContractType).value

                drilling_job_dict = {
                    "proposed_job": {
                        "kkks_id": kkks_id,
                        "area_id": area_id,
                        "field_id": field_id,
                        "contract_type": contract_type,
                        "afe_number": f'AFE0{j}' if contract_type == 'COST-RECOVERY' else '-',
                        "wpb_year": 2024,
                        "start_date": plan_start.date(),
                        "end_date": (plan_start+timedelta(days=20)).date(),
                        "total_budget": round(random.uniform(9999999, 999999),2),
                        "rig_name": f'RIG0{j}',
                        "rig_type": random_enum_value(RigType).value,
                        "rig_horse_power": random.randint(100, 5000),
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
                            "file_id": "string",
                            "title": "string",
                            "creator_name": "string",
                            "create_date": "2024-08-24T13:50:55.638Z",
                            "media_type": "EXTERNAL_HARDDISK",
                            "document_type": "string",
                            "item_category": "string",
                            "item_sub_category": "string",
                            "digital_format": "string",
                            "original_file_name": "string",
                            "digital_size": 0,
                            "digital_size_uom": "BYTE",
                            "remark": "string"
                        }
                        ],
                        "well": {
                            "uwi": f'{i+j}{j}',
                            "field_id": field_id,
                            "area_id": area_id,
                            "kkks_id": kkks_id,
                            "well_name": f'WELL0{i+j}{j}',
                            "alias_long_name": "-",
                            "well_type": random_enum_value(WellType).value,
                            "well_status": random_enum_value(WellStatus).value,
                            "well_profile_type": random_enum_value(WellProfileType).value,
                            "hydrocarbon_target": random_enum_value(HydrocarbonTarget).value,
                            "environment_type": random_enum_value(EnvironmentType).value,
                            "surface_longitude": 106.816666,
                            "surface_latitude": -6.200000,
                            "bottom_hole_longitude": 106.816666,
                            "bottom_hole_latitude": -6.200000,
                            "maximum_inclination": 0,
                            "azimuth": 0,
                            "line_name": "string",
                            "spud_date": "2024-08-24T13:50:55.638Z",
                            "final_drill_date": "2024-08-24T13:50:55.638Z",
                            "completion_date": "2024-08-24T13:50:55.638Z",
                            "rotary_table_elev": 0,
                            "rotary_table_elev_uom": "FEET",
                            "kb_elev": 0,
                            "kb_elev_uom": "FEET",
                            "derrick_floor_elev": 0,
                            "derrick_floor_elev_uom": "FEET",
                            "ground_elev": 0,
                            "ground_elev_uom": "FEET",
                            "mean_sea_level": 0,
                            "mean_sea_level_uom": "FEET",
                            "depth_datum": "RT",
                            "kick_off_point": 0,
                            "kick_off_point_uom": "FEET",
                            "maximum_tvd": 0,
                            "maximum_tvd_uom": "FEET",
                            "final_md": 0,
                            "final_md_uom": "FEET",
                            "remark": "string",
                            "well_documents": [
                                {
                                "file_id": "string",
                                "title": "string",
                                "media_type": "EXTERNAL_HARDDISK",
                                "document_type": "string",
                                "remark": "string"
                                }
                            ],
                            "well_summary": [
                                {
                                "depth_datum": "RT",
                                "depth": 0,
                                "depth_uom": "FEET",
                                "hole_diameter": 0,
                                "hole_diameter_uom": "INCH",
                                "bit": "string",
                                "casing_outer_diameter": 0,
                                "casing_outer_diameter_uom": "INCH",
                                "logging": "string",
                                "mud_program": "string",
                                "cementing_program": "string",
                                "bottom_hole_temperature": 0,
                                "bottom_hole_temperature_uom": "C",
                                "rate_of_penetration": 0,
                                "remarks": "string"
                                }
                            ],
                            "well_test": [
                                {
                                "depth_datum": "RT",
                                "zone_name": "string",
                                "zone_top_depth": 0,
                                "zone_bottom_depth": 0,
                                "depth_uom": "FEET"
                                }
                            ],
                            "well_trajectory": 
                                {
                                "file_id": drilling_trajectory_file_id,
                                "data_format": DataFormat.PLAIN_TEXT,
                                }
                            ,
                            "well_ppfg": 
                                {
                                "file_id": "string",
                                "data_format": "IMAGE",
                                }
                            ,
                            "well_logs": [
                                {
                                "file_id": "string",
                                "data_format": "IMAGE",
                                }
                            ],
                            "well_drilling_parameter": 
                                {
                                "file_id": "string",
                                "data_format": "IMAGE",
                                }
                            ,
                            "well_casing": plan_casing,
                            "well_stratigraphy": [
                                {
                                "depth_datum": "RT",
                                "depth": 0,
                                "depth_uom": "FEET",
                                "stratigraphy_id": "string"
                                }
                            ]
                            }
                        }
                    }

                # wows_job_dict = {
                #     "job": {
                #         "field_id": field_id,
                #         "contract_type": contract_type,
                #         "afe_number": f'AFE0{j}' if contract_type == 'COST-RECOVERY' else '-',
                #         "wpb_year": 2024,
                #         "plan_start": plan_start,
                #         "plan_end": plan_start+timedelta(days=20),
                #         "plan_total_budget": round(random.uniform(9999999, 999999),2),
                #         "rig_name": f'RIG0{j}',
                #         "rig_type": random_enum_value(RigType).value,
                #         "rig_horse_power": random.randint(100, 5000),
                #         "job_activity": [
                #         {
                #             "time": "2024-08-18T01:15:40.565Z",
                #             "measured_depth": 0,
                #             "measured_depth_uoum": "FEET",
                #             "measured_depth_datum": "RT",
                #             "true_vertical_depth": 0,
                #             "true_vertical_depth_uoum": "FEET",
                #             "true_vertical_depth_sub_sea": 0,
                #             "true_vertical_depth_sub_sea_uoum": "FEET",
                #             "daily_cost": 0,
                #             "summary": "string",
                #             "current_operations": "string",
                #             "next_operations": "string"
                #         }
                #         ],
                #         "budget": [
                #         {
                #             "tangible_cost": 0,
                #             "intangible_cost": 0,
                #             "total_cost": 0
                #         }
                #         ],
                #         "work_breakdown_structure": [
                #         {
                #             "event": "string",
                #             "start_date": "2024-08-18T01:15:40.566Z",
                #             "end_data": "2024-08-18T01:15:40.566Z",
                #             "remarks": "string"
                #         }
                #         ],
                #         "drilling_hazard": [
                #         {
                #             "hazard_type": "GAS KICK",
                #             "hazard_description": "string",
                #             "severity": "LOW",
                #             "mitigation": "string",
                #             "remark": "string"
                #         }
                #         ],
                #         "job_documents": [
                #         {
                #             "title": "string",
                #             "creator_name": "string",
                #             "create_date": "2024-08-18T01:15:40.566Z",
                #             "media_type": "EXTERNAL_HARDDISK",
                #             "document_type": "string",
                #             "item_category": "string",
                #             "item_sub_category": "string",
                #             "digital_format": "string",
                #             "original_file_name": "string",
                #             "digital_size": 0,
                #             "digital_size_uom": "BYTE",
                #             "remark": "string"
                #         }
                #         ],
                #         "wows_class": random_enum_value(WOWSClass).value,
                #         "job_category": random_enum_value(WOWSJobType).value,
                #         "current_oil": random.randint(10,20),
                #         "current_gas": random.randint(10,20),
                #         "current_condensate": random.randint(10,20),
                #         "current_oil_water_cut": random.randint(10,20),
                #         "current_gas_water_cut": random.randint(10,20),
                #         "current_condensate_water_cut": random.randint(10,20),
                #         "target_oil": random.randint(40,50),
                #         "target_gas": random.randint(40,50),
                #         "target_condensate": random.randint(40,50),
                #         "target_oil_water_cut": random.randint(0,4),
                #         "target_gas_water_cut": random.randint(0,4),
                #         "target_condensate_water_cut": random.randint(0,4),
                #         "well": {
                #             "uwi": f'{i+j}{j}',
                #             "field_id": field_id,
                #             "well_name": f'WELL0{i+j}{j}',
                #             "alias_long_name": "-",
                #             "well_type": random_enum_value(WellType).value,
                #             "well_class": random_enum_value(WellClass).value,
                #             "well_status": random_enum_value(WellStatus).value,
                #             "profile_type": random_enum_value(ProfileType).value,
                #             "environment_type": random_enum_value(EnvironmentType).value,
                #             "surface_longitude": 0,
                #             "surface_latitude": 0,
                #             "bottom_hole_longitude": 0,
                #             "bottom_hole_latitude": 0,
                #             "maximum_inclination": 0,
                #             "maximum_azimuth": 0,
                #             "line_name": "string",
                #             "spud_date": "2024-08-18T15:38:55.620Z",
                #             "final_drill_date": "2024-08-18T15:38:55.620Z",
                #             "completion_date": "2024-08-18T15:38:55.620Z",
                #             "rotary_table_elev": 0,
                #             "rotary_table_elev_ouom": "FEET",
                #             "kb_elev": 0,
                #             "kb_elev_ouom": "FEET",
                #             "derrick_floor_elev": 0,
                #             "derrick_floor_elev_ouom": "FEET",
                #             "ground_elev": 0,
                #             "ground_elev_ouom": "FEET",
                #             "mean_sea_level": 0,
                #             "mean_sea_level_ouom": "RT",
                #             "depth_datum": "RT",
                #             "kick_off_point": 0,
                #             "kick_off_point_ouom": "FEET",
                #             "drill_td": 0,
                #             "drill_td_ouom": "FEET",
                #             "log_td": 0,
                #             "log_td_ouom": "FEET",
                #             "max_tvd": 0,
                #             "max_tvd_ouom": "FEET",
                #             "projected_depth": 0,
                #             "projected_depth_ouom": "FEET",
                #             "final_td": 0,
                #             "final_td_ouom": "FEET",
                #             "remark": "string",
                #             "well_documents": [
                #                 {
                #                 "file_id": "string",
                #                 "title": "string",
                #                 "media_type": "EXTERNAL_HARDDISK",
                #                 "document_type": "string",
                #                 "remark": "string"
                #                 }
                #             ],
                #             "well_casings": [
                #                 {
                #                 "casing_type": "CONDUCTOR PIPE",
                #                 "grade": "string",
                #                 "inside_diameter": 0,
                #                 "inside_diameter_ouom": "INCH",
                #                 "outside_diameter": 0,
                #                 "outside_diameter_ouom": "INCH",
                #                 "depth_datum": 'KB',
                #                 "top_depth": 0,
                #                 "bottom_depth": 0,
                #                 "depth_uoum": 'FEET',
                #                 }
                #             ],
                #             "well_trajectories": [
                #                 {
                #                 "file_id": "string"
                #                 }
                #             ],
                #             "well_ppfgs": [
                #                 {
                #                 "file_id": "string"
                #                 }
                #             ],
                #             "well_logs": [
                #                 {
                #                 "file_id": "d4336cd0-313b-4114-b27e-4894bb9c2197"
                #                 }
                #             ],
                #             "well_drilling_parameters": [
                #                 {
                #                 "file_id": "string"
                #                 }
                #             ],
                #             "well_strat": [
                #                 {
                #                 "strat_unit_id": "string",
                #                 "depth_datum": "RT",
                #                 "top_depth": 0,
                #                 "bottom_depth": 0,
                #                 "depth_uoum": "FEET"
                #                 }
                #             ]
                #             }
                #     }
                # }
            
                # create_pengajuan_wows(
                #     db,
                #     CreatePengajuanWOWS(**wows_job_dict),
                #     GetUser.model_validate(user)
                # )
                
                    
                db_plan = job_models.Planning(
                    **job_crud.parse_schema(job_crud.CreateExplorationPlanning(**drilling_job_dict))
                )

                db_plan.date_proposed = datetime.now().date()
                db_plan.status = job_models.PlanningStatus.PROPOSED

                db_plan.proposed_job.job_instance_type = job_models.JobInstanceType.INITIAL_PROPOSAL

                db_plan.proposed_job.well.kkks_id = kkks_id
                db_plan.proposed_job.kkks_id = kkks_id

                db_plan.proposed_job.well.area_id = area_id
                db_plan.proposed_job.well.field_id = field_id

                db_plan.proposed_job.well.well_instance_type = WellInstanceType.INITIAL_PROPOSAL

                db_plan.created_by_id = user_id
                db_plan.time_created = datetime.now()

                db.add(db_plan)
            
        db.commit()
