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

def get_combined_data(db: Session) -> List[Dict]:
    try:
        # Query untuk mendapatkan semua well names
        wells = db.query(Well.id, Well.well_name).all()
        
        # Query untuk mendapatkan semua job plans dengan status
        job_plans = db.query(Planning.id, Planning.proposed_job_id, Planning.status).all()
        
        # Query untuk mendapatkan semua jobs dengan start_date
        jobs = db.query(Job.id, Job.start_date).all()
        
        # Membuat dictionary untuk mempercepat lookup
        well_dict = {w.id: w.well_name for w in wells}
        job_plan_dict = {jp.proposed_job_id: (jp.id, jp.status) for jp in job_plans}
        job_dict = {j.id: j.start_date for j in jobs}
        
        # Menggabungkan data
        combined_data = []
        for job_id, start_date in job_dict.items():
            well_name = None
            job_plan_id = None
            plan_status = None
            
            # Mendapatkan job plan id dan status
            if job_id in job_plan_dict:
                job_plan_id, plan_status = job_plan_dict[job_id]
            
            # Mencari well_name yang sesuai (asumsi ada relasi antara Job dan Well melalui field_id)
            job = db.query(Job).filter(Job.id == job_id).first()
            if job and job.field_id:
                well = db.query(Well).filter(Well.field_id == job.field_id).first()
                if well:
                    well_name = well.well_name
            
            combined_data.append({
                "well_name": well_name,
                "job_plan_id": job_plan_id,
                "job_start_date": start_date,
                "plan_status": plan_status
            })
        
        return combined_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    try:
        # Query untuk mendapatkan semua well names
        wells = db.query(Well.id, Well.well_name).all()
        
        # Query untuk mendapatkan semua job plans
        job_plans = db.query(Planning.id, Planning.proposed_job_id).all()
        
        # Query untuk mendapatkan semua jobs dengan start_date
        jobs = db.query(Job.id, Job.start_date).all()
        
        # Membuat dictionary untuk mempercepat lookup
        well_dict = {w.id: w.well_name for w in wells}
        job_plan_dict = {jp.proposed_job_id: jp.id for jp in job_plans}
        job_dict = {j.id: j.start_date for j in jobs}
        
        # Menggabungkan data
        combined_data = []
        for job_id, start_date in job_dict.items():
            well_name = None
            job_plan_id = job_plan_dict.get(job_id)
            
            # Mencari well_name yang sesuai (asumsi ada relasi antara Job dan Well melalui field_id)
            job = db.query(Job).filter(Job.id == job_id).first()
            if job and job.field_id:
                well = db.query(Well).filter(Well.field_id == job.field_id).first()
                if well:
                    well_name = well.well_name
            
            combined_data.append({
                "well_name": well_name,
                "job_plan_id": job_plan_id,
                "job_start_date": start_date
            })
        
        return combined_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
def get_all_data(db: Session):
    return get_combined_data(db)

