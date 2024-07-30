from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
