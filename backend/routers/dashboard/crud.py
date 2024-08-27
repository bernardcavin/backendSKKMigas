from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends, HTTPException
from backend.routers.job.models import *
from backend.routers.job.schemas import *
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

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Dict
from datetime import date

def get_combined_data(db: Session) -> List[Dict]:
    try:
        # Query untuk mendapatkan semua well names
        wells = db.query(Well.id, Well.well_name).all()
        
        # Query untuk mendapatkan semua job plans dengan status dan date_proposed
        job_plans = db.query(Planning.id, Planning.proposed_job_id, Planning.date_proposed, Planning.status).all()
        
        # Query untuk mendapatkan semua jobs dengan start_date dan end_date
        jobs = db.query(Job.id, Job.start_date, Job.end_date, Job.field_id).all()
        
        # Membuat dictionary untuk mempercepat lookup
        well_dict = {w.id: w.well_name for w in wells}
        job_plan_dict = {jp.proposed_job_id: (jp.id, jp.date_proposed, jp.status) for jp in job_plans}
        
        # Menggabungkan data
        combined_data = []
        for job in jobs:
            well_name = None
            job_plan_id = None
            date_proposed = None
            plan_status = None
            
            # Mendapatkan job plan id, date_proposed, dan status
            if job.id in job_plan_dict:
                job_plan_id, date_proposed, plan_status = job_plan_dict[job.id]
            
            # Mencari well_name yang sesuai
            if job.field_id:
                well = db.query(Well).filter(Well.field_id == job.field_id).first()
                if well:
                    well_name = well.well_name
            
            combined_data.append({
                "well_name": well_name,
                "job_plan_id": job_plan_id,
                "job_start_date": job.start_date,
                "job_end_date": job.end_date,
                "plan_date_proposed": date_proposed,
                "plan_status": plan_status
            })
        
        return combined_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Penggunaan fungsi
def get_all_data(db: Session):
    return get_combined_data(db)

