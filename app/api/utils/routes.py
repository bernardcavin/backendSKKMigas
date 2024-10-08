from fastapi import APIRouter, Depends, File, UploadFile
from typing import List
from sqlalchemy.orm import Session
from app.api.auth.models import Role
from app.core.security import authorize, get_db, get_current_user
from app.api.utils.schemas import TabularData,DrillingOperationResponse,BHAResponse
from app.api.job.models import *
from app.api.utils.crud import *
from well_profile import load
from app.core.schema_operations import create_api_response
from app.api.visualize.lib.well_profile_func import render_well_profile

router = APIRouter(prefix="/utils", tags=["utils"])

@router.post("/upload/file", tags=['file'])
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
        print(e)
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

    file_info = save_upload_file(db, file, user)
    
    try:
        well_profile = load(file_info.file_location)
        fig_data = render_well_profile(well_profile)

        return create_api_response(
            success=True,
            message="Trajectory file uploaded and processed successfully",
            data={"file_info": file_info, "plot": fig_data}
        )
        
    except Exception as e:
        
        return create_api_response(
            success=True,
            message="Trajectory file uploaded successfully",
        )
    
@router.get("/drilling-operations/pyenum", response_model=List[DrillingOperationResponse])
async def list_drilling_operations():
    return [
        DrillingOperationResponse(operation=op, description=op.value)
        for op in DrillingOperation
    ]

@router.get("/bha/pyenum", response_model=List[BHAResponse])
async def list_bhacomponents():
    return [
       BHAResponse(bhacomponent=op)
        for op in BHAComponentType
    ]
    
@router.post("/wbs/upload-excel/")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Memeriksa apakah file adalah Excel
    return excel_wbs(file, db)
@router.post("/drillingfluid/upload-excell/")
async def upload_excel_drillingfluid(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_drillingfluid(file, db)
@router.post("/mudaddictive/upload-excell/")
async def upload_excel_mudaddictive(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_mudadditive(file, db)
@router.post("/bulk-material/upload-excell/")
async def upload_excel_bulkmaterial(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_bulkmaterial(file, db)
@router.post("/directionalsurvey/upload-excell/")
async def upload_excel_directionalsurvey(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_directionalsurvey(file, db)
@router.post("/personnel/upload-excell/")
async def upload_excel_personnel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_personnel(file, db)
@router.post("/pumps/upload-excell/")
async def upload_excel_pumps(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_pumps(file, db)
@router.post("/weather/upload-excell/")
async def upload_excel_weather(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_weather(file, db)
@router.post("/wellsummary/upload-excell/")
async def upload_excel_wellsummary(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_well_summary(file, db)
@router.post("/wellcasing/upload-excell/")
async def upload_excel_wellcasing(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_well_casing(file, db)
@router.post("/wellstatigraphy/upload-excell/")
async def upload_excel_wellstatigraphy(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_well_stratigraphy(file, db)
@router.post("/welltest/upload-excell/")
async def upload_excel_welltest(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_well_test(file, db)
@router.post("/jobhazard/upload-excell/")
async def upload_excel_jobhazard(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_job_hazard(file, db)
@router.post("/joboperationdays/upload-excell/")
async def upload_excel_joboperationdays(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_job_operation_day(file, db)
@router.post("/jobdocument/upload-excell/")
async def upload_excel_jobdocument(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return excel_job_document(file, db)