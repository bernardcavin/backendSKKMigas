from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers.auth import routers as auth_routers
from backend.routers.job import routers as job_routers
from backend.routers.geometry import routers as geometry_routers
from backend.routers.well import routers as well_routers
from backend.routers.utils import routers as utils_routers
from backend.routers.dashboard import routers as dashboard_routers
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

import os

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

if int(os.getenv('DEMO_MODE'))==1:
    logger.info('Creating dummy data')
    from backend.utils.create_dummy_data import generate_dummy_data
    if os.path.exists('test.db'):
        os.remove("test.db")
    Base.metadata.create_all(bind=engine)
    generate_dummy_data(n=1)
    logger.info('Dummy data successfully created')
else:
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:8000"],  # Ganti dengan URL frontend Anda
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(auth_routers.router)
app.include_router(job_routers.router)
app.include_router(geometry_routers.router)
app.include_router(well_routers.router)
app.include_router(utils_routers.router)
app.include_router(dashboard_routers.router)