from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth import routers as auth_routers
from app.routers.job import routers as job_routers
from app.routers.geometry import routers as geometry_routers

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routers.router)
app.include_router(job_routers.router)
app.include_router(geometry_routers.router)