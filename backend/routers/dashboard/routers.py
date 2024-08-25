from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, extract, and_, cast, Integer
from sqlalchemy.orm import Session
from typing import Dict,List
from backend.routers.auth.models import Role
from backend.routers.job.models import *
from backend.routers.well.schemas import *
from backend.routers.well.models import *
from backend.routers.auth.schemas import GetUser
from backend.routers.dashboard.crud import *
from calendar import monthrange, month_name as calendar_month_name
from datetime import datetime,timedelta
import plotly.graph_objects as go
import numpy as np

from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas, models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])



@router.get("/job-counts", response_model=Dict[str, int])
async def get_job_counts(db: Session = Depends(get_db)):
    try:
        counts = count_job_data(db)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/job-well-data", response_model=CombinedData)
async def read_job_and_well_data(db: Session = Depends(get_db)):
    try:
        well_data = get_well_names(db)
        job_data = get_job_data(db)
        return CombinedData(wells=well_data, jobs=job_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    


