from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth import routers as auth_routers
from app.routers.job import routers as job_routers
from app.routers.geometry import routers as geometry_routers
from app.routers.well import routers as well_routers
from app.routers.utils import routers as utils_routers
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:8000"],  # Ganti dengan URL frontend Anda
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routers.router)
app.include_router(job_routers.router)
app.include_router(geometry_routers.router)
app.include_router(well_routers.router)
app.include_router(utils_routers.router)