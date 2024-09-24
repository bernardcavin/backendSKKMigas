from posixpath import sep
from fastapi import UploadFile, HTTPException
import shutil
import os
from datetime import datetime
from app.api.utils.schemas import *
from sqlalchemy.orm import Session
from app.api.auth.schemas import GetUser
from app.api.utils.models import *
import pandas as pd

from app.core.config import settings
from uuid import uuid4
import os



def save_upload_file(db: Session, upload_file: UploadFile, user) -> FileInfo:
    
    if os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir, exist_ok=True)
    
    try:
    
        file_id = str(uuid4())
        file_extension = os.path.splitext(upload_file.filename)[1]
        file_location = os.path.join(settings.upload_dir, f'{file_id}{file_extension}')
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file")

    try:
        db_file = FileDB(
            id=file_id,
            filename=upload_file.filename,
            file_location=file_location,
            file_extension=file_extension,
            uploaded_by_id=user.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    
    except Exception as e:
        os.remove(file_location)
        raise HTTPException(status_code=500, detail="Failed to save file")

    return FileInfo.model_validate(db_file)
    
def save_upload_multiple_files(db: Session, upload_files: List[UploadFile], user) -> List[FileInfo]:

    file_objs = []
    file_locations = []

    if os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir, exist_ok=True)

    for upload_file in upload_files:
        try:
            file_id = str(uuid4())
            file_extension = os.path.splitext(upload_file.filename)[1]
            file_location = os.path.join(settings.upload_dir, f'{file_id}{file_extension}')
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(upload_file.file, file_object)
            file_locations.append(file_location)
            
        except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to upload files")

        try:
            db_file = FileDB(
                id=file_id,
                filename=upload_file.filename,
                file_location=file_location,
                file_extension=file_extension,
                uploaded_by_id=user.id
            )
            file_objs.append(db_file)
        
        except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to save files")

    try:
        db.add_all(file_objs)
        db.commit()
    except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to save files")

    return [FileInfo.model_validate(file_obj) for file_obj in file_objs]

def jsonify_tabular_file(file: UploadFile):

    if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file.file.read(), engine='openpyxl')
    elif file.content_type == 'text/csv':
        df = pd.read_csv(file.file, sep=';')
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    records = df.to_dict(orient = "records")

    return TabularData(headers=df.columns.to_list(), records=records)