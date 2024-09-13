from posixpath import sep
from fastapi import UploadFile, HTTPException
import shutil
import os
from datetime import datetime
from app.api.utils.schemas import *
from sqlalchemy.orm import Session, with_polymorphic
from app.api.auth.schemas import GetUser
from app.api.well.models import *
import pandas as pd

def get_well_data(data_class: DataClass, db: Session, well_id: str):
    return db.query(WellDigitalData).filter(WellDigitalData.data_class == data_class, WellDigitalData.well_id == well_id).first()

