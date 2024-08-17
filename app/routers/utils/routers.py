from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import *
import json

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get('/roles/{role_name}')
async def get_roles(role_name: str):
    return {Role.__members__.get(role_name.upper())}