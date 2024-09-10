from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers.auth import routers as auth_routers
from backend.routers.job import routers as job_routers
from backend.routers.spatial import routers as spatial_routers
from backend.routers.well import routers as well_routers
from backend.routers.utils import routers as utils_routers
from backend.routers.dashboard import routers as dashboard_routers
from backend.routers.visualize import routers as visualization_routers
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import contextlib
from backend.database import SessionLocal
from sqlalchemy.orm import Session
from backend.routers.auth.models import User
from backend.utils.create_dummy_data import generate_dummy_data

import os

app = FastAPI()

def reset_database(engine):
    Base.metadata.drop_all(bind=engine)  # Drops all tables
    Base.metadata.create_all(bind=engine)  # Creates all tables
    
def data_exists(db: Session):
    return db.query(User).first() is not None
    
@contextlib.contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Main logic for generating dummy data if no data exists
def handle_data_creation(engine, demo_mode=False):
    with get_db_context() as session:
        try:
            if data_exists(session):
                pass

        except:
            reset_database(engine)

            if demo_mode:
                generate_dummy_data(session, n=500)

if int(os.getenv('DEMO_MODE', 0)) == 1:
    handle_data_creation(engine, demo_mode=True)
else:
    handle_data_creation(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:8000","http://localhost:4173"],  # Ganti dengan URL frontend Anda
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(auth_routers.router)
app.include_router(job_routers.router)
app.include_router(spatial_routers.router)
app.include_router(well_routers.router)
app.include_router(utils_routers.router)
app.include_router(dashboard_routers.router)
app.include_router(visualization_routers.router)