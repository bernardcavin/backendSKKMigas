from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.routers.job.models import Eksplorasi,Eksploitasi, Workover, WellService, TipePekerjaan, LogPekerjaan
from app.routers.job.schemas import Job, LogPekerjaanSchema

from typing import Union

type_map = {
    TipePekerjaan.EKSPLORASI : Eksplorasi,
    TipePekerjaan.EKSPLOITASI : Eksploitasi,
    TipePekerjaan.WORKOVER : Workover,
    TipePekerjaan.WELLSERVICE : WellService,
}

def create_job(db: Session, job: Job ):
    
    db_job = type_map[job.tipe_pekerjaan](
        **job.model_dump()
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def create_job_log(db: Session, job_log: LogPekerjaanSchema ):
    
    db_job_log = LogPekerjaan(
        **job_log.model_dump()
    )
    db.add(db_job_log)
    db.commit()
    db.refresh(db_job_log)
    return db_job_log
