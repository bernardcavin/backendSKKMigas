from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import *
import json
from app.routers.geometry.models import *
from app.routers.job.models import DataPhase, Severity

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get('/roles')
async def get_roles():
    return {role.value for role in Role}
@router.get('/areaphase')
async def get_areaphase():
    return {areaphase.value for areaphase in AreaPhase}

@router.get('/areatype')
async def get_areatype():
    return {areatype.value for areatype in AreaType}

@router.get('/areaposition')
async def get_areaposition():
    return {areaposition.value for areaposition in AreaPosition}

@router.get('/areaproductionstatus')
async def get_areaproductionstatus():
    return {areaproductionstatus.value for areaproductionstatus in AreaProductionStatus}

@router.get('/arearegion')
async def get_arearegion():
    return {arearegion.value for arearegion in AreaRegion}

@router.get('/strattype')
async def get_strattype():
    return {strattype for strattype in StratType}

@router.get('/stratunittype')
async def get_stratunittype():
    return {stratunittype.value for stratunittype in StratUnitType}

@router.get('/petroleumsystem')
async def get_petroleumsystem():
    return {petroleumsystem.value for petroleumsystem in PetroleumSystem}

@router.get('/dataphase')
async def get_dataphase():
    return {dataphase.value for dataphase in DataPhase}

@router.get('/severity')
async def get_severity():
    return {severity.value for severity in Severity}

