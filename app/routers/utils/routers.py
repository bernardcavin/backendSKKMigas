from fastapi import APIRouter, Depends, HTTPException, status,File,UploadFile
import shutil
from typing import List
from sqlalchemy.orm import Session
from app.routers.auth.models import *
import json
import os
from app.routers.geometry.models import *
from app.routers.job.models import ContractType, DataPhase, DrillingClass, HazardType, JobType, RigType, Severity, StatusCloseOut, StatusOperasi, StatusPPP, StatusPengajuan, WOWSClass, WOWSJobType
from app.routers.well.models import CasingType, CasingUOM, DENLogUOM, DepthDatum, DepthUOM, EnvironmentType, LogType, MediaType, PORLogUOM, ProfileType, SizeUOM, VolumeUOM, WellType
from app.routers.utils.schemas import *
from app.routers.utils.crud import *
from app.routers.auth.utils import authorize, get_db, get_current_user

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

enum_map = {
    "roles": Role,
    "depth_datum": DepthDatum,
    "area_phase": AreaPhase,
    "area_type": AreaType,
    "area_position": AreaPosition,
    "area_production_status": AreaProductionStatus,
    "area_region": AreaRegion,
    "strat_type": StratType,
    "strat_unit_type": StratUnitType,
    "petroleum_system": PetroleumSystem,
    "data_phase": DataPhase,
    "severity": Severity,
    "status_pengajuan": StatusPengajuan,
    "status_operasi": StatusOperasi,
    "status_ppp": StatusPPP,
    "status_closeout": StatusCloseOut,
    "job_type": JobType,
    "contract_type": ContractType,
    "rig_type": RigType,
    "hazard_type": HazardType,
    "wows_job_type": WOWSJobType,
    "drilling_class": DrillingClass,
    "wows_class": WOWSClass,
    "environment": EnvironmentType,
    "well_type": WellType,
    "profile_type": ProfileType,
    "well_class": WOWSClass,
    "casing_uom": CasingUOM,
    "casing_type": CasingType,
    "depth_uom": DepthUOM,
    "volume_uom": VolumeUOM,
    "media_type": MediaType,
    "size_uom": SizeUOM,
    "log_type": LogType,
    "denlog_uom": DENLogUOM,
    "porlog_uom": PORLogUOM
}

@router.get('/enum/get/{enum_name}')
async def get_enum_values(enum_name: str):

    enum_class = enum_map.get(enum_name)

    if enum_class is None:
        raise HTTPException(status_code=404, detail="Enum not found")
    
    return {item.value for item in enum_class}

@router.get('/enum/all')
async def get_all_enum_values():
    all_enum_values = {}
    for key, enum_class in enum_map.items():
        all_enum_values[key] = {item.value for item in enum_class}
    return all_enum_values
