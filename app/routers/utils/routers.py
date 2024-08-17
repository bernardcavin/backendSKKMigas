from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import *
import json

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get('/roles')
async def get_roles():
    return {role.value for role in Role}