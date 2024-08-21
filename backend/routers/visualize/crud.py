from posixpath import sep
from fastapi import UploadFile, HTTPException
import shutil
import os
from datetime import datetime
from backend.routers.utils.schemas import *
from sqlalchemy.orm import Session, with_polymorphic
from backend.routers.auth.schemas import GetUser
from backend.routers.well.models import *
import pandas as pd

def get_well_data(data_class: DataClass, db: Session, well_id: str):
    return db.query(WellDigitalData).filter(WellDigitalData.data_class == data_class, WellDigitalData.well_id == well_id).first()