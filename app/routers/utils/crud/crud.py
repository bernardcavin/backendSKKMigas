from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import shutil
import os
from datetime import datetime
from app.routers.utils.schemas import *


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
UPLOAD_DIR = os.path.join(BASE_DIR, "upload")
def save_upload_file(upload_file: UploadFile) -> FileInfo:
    try:
        file_location = os.path.join(UPLOAD_DIR, upload_file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)
        
        file_info = FileInfo(
            filename=upload_file.filename,
            size=os.path.getsize(file_location),
            content_type=upload_file.content_type,
            upload_time=datetime.now()
        )
        return file_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))