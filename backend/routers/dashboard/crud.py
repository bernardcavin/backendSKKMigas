from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends, HTTPException
from backend.routers.job.models import *
from backend.routers.well.crud import *
from backend.routers.well.schemas import *
from backend.routers.dashboard.schemas import *
from backend.routers.auth.schemas import GetUser
from backend.routers.well.models import *

from typing import Union

def count_job_data(db: Session) -> Dict[str, int]:
    operations_count = db.query(func.count(Operation.id)).scalar()
    ppp_count = db.query(func.count(PPP.id)).scalar()
    closeout_count = db.query(func.count(CloseOut.id)).scalar()

    return {
        "job_operations": operations_count,
        "job_ppp": ppp_count,
        "job_closeout": closeout_count
    }

def get_well_names(db: Session) -> List[WellData]:
    try:
        wells = db.query(Well.well_name).all()
        return [WellData(well_name=well.well_name) for well in wells]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in wells: {str(e)}")

def get_job_data(db: Session) -> List[JobData]:
    try:
        jobs = db.query(Job.start_date).all()
        return [JobData(start_date=job.start_date) for job in jobs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error in jobs: {str(e)}")

