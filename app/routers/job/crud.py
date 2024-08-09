from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.routers.job.models import Eksplorasi,Eksploitasi, Workover, WellService, TipePekerjaan
from app.routers.job.schemas import Job

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
