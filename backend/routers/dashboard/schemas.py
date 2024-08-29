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
    well_name: Optional[str]

    class Config:
        from_attributes = True

class JobData(BaseModel):
    start_date: Optional[date]

    class Config:
        from_attributes = True

class CombinedData(BaseModel):
    wells: List[WellData]
    jobs: List[JobData]


class JobTypeData(BaseModel):
    count: int
    approved: int
    active: int
    percentage: float

class JobTypeData(BaseModel):
    approved_plans: int
    active_operations: int
    percentage: float

class KKKSJobData(BaseModel):
    id: str
    nama_kkks: str
    exploration: JobTypeData
    development: JobTypeData
    workover: JobTypeData
    wellservice: JobTypeData

class JobTypeDataUP(BaseModel):
    total: int
    plan: int
    realization: int
    percentage: float
    change: int

class AggregateJobData(BaseModel):
    exploration: JobTypeDataUP
    development: JobTypeDataUP
    workover: JobTypeDataUP
    wellservice: JobTypeDataUP

class JobTypeSummary(BaseModel):
    job_type: str
    rencana: int
    realisasi: int
    selesai: int