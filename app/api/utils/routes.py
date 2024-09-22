from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.core.security import authorize, get_db, get_current_user
from app.api.spatial.models import Lapangan as OilField
from app.api.job.models import ContractType, HazardType, RigType, Severity, WOWSJobType
from app.api.well.models import CasingType, DepthDatum, EnvironmentType, LogType, MediaType, WellType, WellStatus, WellProfileType
from app.api.utils.schemas import UploadResponse, MultiUploadResponse, TabularData
from app.api.utils.crud import save_upload_file, save_upload_multiple_files, jsonify_tabular_file
from app.api.auth.schemas import GetUser
from well_profile import load
import json
import pandas as pd
import plotly.graph_objects as go
from app.core.schema_operations import create_api_response
from app.api.visualize.lib.well_profile_func import render_well_profile

router = APIRouter(prefix="/utils", tags=["utils"])

@router.post("/upload/file")
@authorize(role=[Role.Admin, Role.KKKS])
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        file_info = save_upload_file(db, file, user)
        return create_api_response(
            success=True,
            message=f"File '{file.filename}' uploaded successfully",
            data={"file_info": file_info}
        )
    except Exception as e:
        return create_api_response(success=False, message="Failed to upload file", status_code=500)

@router.post("/upload/files")
@authorize(role=[Role.Admin, Role.KKKS])
async def create_upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        file_infos = save_upload_multiple_files(db, files, user)
        return create_api_response(
            success=True,
            message=f"Successfully uploaded {len(files)} files",
            data={"files_info": file_infos}
        )
    except Exception as e:
        return create_api_response(success=False, message="Failed to upload files", status_code=500)

@router.post("/read/tabular", response_model=TabularData)
@authorize(role=[Role.Admin, Role.KKKS])
async def read_tabular_file(file: UploadFile = File(...), user = Depends(get_current_user)):
    try:
        tabular_data = jsonify_tabular_file(file)
        return create_api_response(success=True, message="Tabular file read successfully", data=tabular_data)
    except Exception as e:
        return create_api_response(success=False, message="Failed to read tabular file", status_code=500)

@router.post("/upload/trajectory")
async def upload_trajectory_file(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        file_info = save_upload_file(db, file, user)
        well_profile = load(file_info.file_location)
        
        fig_data = render_well_profile(well_profile)

        return create_api_response(
            success=True,
            message="Trajectory file uploaded and processed successfully",
            data={"file_info": file_info, "plot": fig_data}
        )
    except Exception as e:
        return create_api_response(success=False, message="File cannot be processed", status_code=500)
