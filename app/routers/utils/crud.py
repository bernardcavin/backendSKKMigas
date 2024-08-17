from posixpath import sep
from fastapi import UploadFile, HTTPException
import shutil
import os
from datetime import datetime
from app.routers.utils.schemas import *
from sqlalchemy.orm import Session
from app.routers.auth.schemas import GetUser
from app.routers.utils.models import *
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
UPLOAD_DIR = os.path.join(BASE_DIR, os.getenv("UPLOAD_DIR"))

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(db: Session, upload_file: UploadFile, user: GetUser) -> FileInfo:

    file_location = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)

    db_file = FileDB(
        filename=upload_file.filename,
        size=os.path.getsize(file_location),
        content_type=upload_file.content_type,
        upload_time=datetime.now(),
        file_location=file_location,
        uploaded_by_id=user.id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return FileInfo.model_validate(db_file)
    
def save_upload_multiple_files(db: Session, upload_files: List[UploadFile], user: GetUser) -> List[FileInfo]:

    file_objs = []

    for upload_file in upload_files:
        file_location = os.path.join(UPLOAD_DIR, upload_file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)

        db_file = FileDB(
            filename=upload_file.filename,
            size=os.path.getsize(file_location),
            content_type=upload_file.content_type,
            upload_time=datetime.now(),
            file_location=file_location,
            uploaded_by_id=user.id
        )

        file_objs.append(db_file)

    db.add_all(file_objs)
    db.commit()
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