from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from pydantic import BaseModel
from datetime import date
from backend.routers.job.schemas import *
from backend.routers.well.schemas import *


from .schemas import WellBase, JobBase  # Assuming you have these in your schemas

router = APIRouter()

class WellData(BaseModel):
    well_name: str | None

    class Config:
        orm_mode = True

class JobData(BaseModel):
    start_date: date | None

    class Config:
        orm_mode = True

class CombinedData(BaseModel):
    wells: List[WellData]
    jobs: List[JobData]
