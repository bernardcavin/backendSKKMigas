from fastapi import APIRouter, Depends, HTTPException, File,UploadFile
from typing import List
from sqlalchemy.orm import Session
from backend.routers.auth.models import *
from backend.routers.spatial.models import *
from backend.routers.spatial.models import Lapangan as OilField
from backend.routers.job.models import ContractType, HazardType, RigType, Severity, WOWSJobType
from backend.routers.well.models import CasingType, DepthDatum, EnvironmentType, LogType, MediaType, WellType, WellStatus, WellProfileType
from backend.routers.utils.schemas import *
from backend.routers.utils.crud import *
from backend.routers.auth.utils import authorize, get_db, get_current_user

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.routers.auth.models import *
from backend.routers.job.models import *
from backend.routers.job.schemas import *
from backend.routers.well.crud import *
from backend.routers.well.schemas import *
from backend.routers.spatial.models import Area
from backend.routers.spatial.schemas import *
from backend.routers.auth.schemas import GetUser
from backend.routers.well.models import *
from typing import List
from well_profile import load
import json

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

router = APIRouter(prefix="/utils", tags=["utils"])

@router.post("/upload/file", response_model=UploadResponse)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    file_info = save_upload_file(db, file, user)
    return UploadResponse(
        message=f"File '{file.filename}' uploaded successfully",
        file_info=file_info
    )

@router.post("/upload/files", response_model=MultiUploadResponse)
@authorize(role=[Role.Admin, Role.KKKS])
async def create_upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    file_infos = save_upload_multiple_files(db, files, user)
    
    return MultiUploadResponse(
        message=f"Successfully uploaded {len(files)} files",
        files_info=file_infos
    )

@router.post("/read/tabular", response_model=TabularData)
@authorize(role=[Role.Admin, Role.KKKS])
async def read_tabular_file(file: UploadFile = File(...), user: GetUser = Depends(get_current_user)):
    return jsonify_tabular_file(file)

@router.post("/upload/trajectory")
async def upload_trajectory_file(file: UploadFile = File(...), db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    
    try:
        file_info = save_upload_file(db, file, user)
        well_profile = load(file_info.file_location)
        well_profile_df = pd.DataFrame(well_profile.trajectory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File cannot be processed.")
    
    fig = go.Figure(
        data=[go.Scatter3d(x=well_profile_df['east'],
                            y=well_profile_df['north'],
                            z=well_profile_df['tvd'],
                            mode='markers',
                            marker=dict(
                                showscale=True,
                                opacity=0.8),
                            legendgroup=True,
                            hovertemplate='%{text}<extra></extra><br>' + '<b>North</b>: %{y:.2f}<br>' +
                                            '<b>East</b>: %{x}<br>' + '<b>TVD</b>: %{z}<br>',
                           )])

    fig.update_layout(scene=dict(
        xaxis_title='East',
        yaxis_title='North',
        zaxis_title='TVD',
        aspectmode='manual'))

    fig.update_scenes(zaxis_autorange="reversed")
    fig.update_layout(title='Wellbore Trajectory - 3D View')
    
    fig.update_layout(template='plotly_white')
    
    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)

    return {
        'fileinfo':file_info,
        'plot': fig_data
    }

# enum_map = {
#     "roles": Role,
#     "depth_datum": DepthDatum,
#     "phase": AreaPhase,
#     "type": AreaType,
#     "position": AreaPosition,
#     "production_status": AreaProductionStatus,
#     "region": AreaRegion,
#     "strat_type": StratType,
#     "strat_unit_type": StratUnitType,
#     "petroleum_system": PetroleumSystem,
#     "severity": Severity,
#     "contract_type": ContractType,
#     "rig_type": RigType,
#     "hazard_type": HazardType,
#     "wows_job_type": WOWSJobType,
#     "environment": EnvironmentType,
#     "well_type": WellType,
#     "profile_type": WellProfileType,
#     "casing_type": CasingType,
#     "media_type": MediaType,
#     "log_type": LogType,
#     "well_status": WellStatus,
# }

# @router.get('/enum/get/{enum_name}')
# async def get_enum_values(enum_name: str):

#     enum_class = enum_map.get(enum_name)

#     if enum_class is None:
#         raise HTTPException(status_code=404, detail="Enum not found")
    
#     return {item.value for item in enum_class}

# @router.get('/enum/all')
# async def get_all_enum_values():
#     all_enum_values = {}
#     for key, enum_class in enum_map.items():
#         all_enum_values[key] = {item.value for item in enum_class}
#     return all_enum_values

# obj_map = {
#     'kkks': {
#         'obj':KKKS,
#         'key':'name',
#         'value':'id'
#     },
#     'area': {
#         'obj':Area,
#         'key':'label',
#         'value':'id'
#     },
#     'field': {
#         'obj':OilField,
#         'key':'name',
#         'value':'id'
#     },
#     'strat_unit': {
#         'obj':StratUnit,
#         'key':'strat_unit_name',
#         'value':'id'
#     },
# }

# @router.get('/db/get/{obj_name}')
# @authorize(role=[Role.Admin, Role.KKKS])
# async def get_obj(obj_name: str, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):

#     obj_class_dict = obj_map.get(obj_name)

#     if obj_class_dict is None:
#         raise HTTPException(status_code=404, detail="Object not found")
    
#     obj_class = obj_class_dict['obj']

#     objs = db.query(obj_class).all()

#     return {getattr(obj, obj_class_dict['key']) : getattr(obj, obj_class_dict['value']) for obj in objs}

# @router.get('/db/all')
# @authorize(role=[Role.Admin, Role.KKKS])
# async def get_obj(db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
#     all_obj_values = {}
#     for key, obj_class_dict in obj_map.items():

#         obj_class = obj_class_dict['obj']

#         objs = db.query(obj_class).all()

#         all_obj_values[key] = {getattr(obj, obj_class_dict['key']) : getattr(obj, obj_class_dict['value']) for obj in objs}

#     return all_obj_values
