from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers.auth.models import *
import json
from app.routers.geometry.models import *
from app.routers.job.models import ContractType, DataPhase, DrillingClass, HazardType, JobType, RigType, Severity, StatusCloseOut, StatusOperasi, StatusPPP, StatusPengajuan, WOWSClass, WOWSJobType
from app.routers.well.models import CasingType, CasingUOM, DENLogUOM, DepthDatum, DepthUOM, Environment, LogType, MediaType, PORLogUOM, ProfileType, SizeUOM, VolumeUOM, WellType

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

@router.get('/statuspengajuan')
async def get_statuspengajuan():
    return {statuspengajuan.value for statuspengajuan in StatusPengajuan}

@router.get('/statusoperasi')
async def get_statusoperasi():
    return {statusoperasi.value for statusoperasi in StatusOperasi}

@router.get('/statusppp')
async def get_statusppp():
    return {statusppp.value for statusppp in StatusPPP}

@router.get('/statuscloseout')
async def get_statuscloseout():
    return {statuscloseout.value for statuscloseout in StatusCloseOut}

@router.get('/jobtype')
async def get_jobtype():
    return {jobtype.value for jobtype in JobType}

@router.get('/contracttype')
async def get_contracttype():
    return {contracttype.value for contracttype in ContractType}

@router.get('/rigtype')
async def get_rigttype():
    return {rigttype.value for rigttype in RigType}

@router.get('/hazardtype')
async def get_hazardtype():
    return {hazardtype.value for hazardtype in HazardType}

@router.get('/wowsjobtype')
async def get_wowsjobtype():
    return {wowsjobtype.value for wowsjobtype in WOWSJobType}

@router.get('/drilling class')
async def get_drillingclas():
    return {drillingclass.value for drillingclass in DrillingClass}

@router.get('/wowsclass')
async def get_wowsclass():
    return {wowsclass.value for wowsclass in WOWSClass}

@router.get('/environment')
async def get_environment():
    return {environment.value for environment in Environment}

@router.get('/welltype')
async def get_deptdatum():
    return {welltype.value for welltype in WellType}

@router.get('/profiletype')
async def get_profiletype():
    return {profiletype.value for profiletype in ProfileType}

@router.get('/wellclass')
async def get_wowsclass():
    return {wowsclass.value for wowsclass in WOWSClass}

@router.get('/casinguom')
async def get_casinguom():
    return {casinguom.value for casinguom in CasingUOM}

@router.get('/casingtype')
async def get_casingtype():
    return {casingtype.value for casingtype in CasingType}

@router.get('/depthuom')
async def get_depthuom():
    return {depthuom.value for depthuom in DepthUOM}

@router.get('/volumeuom')
async def get_volumeuom():
    return {volumeuom.value for volumeuom in VolumeUOM}

@router.get('/mediatype')
async def get_mediatype():
    return {mediatype.value for mediatype in MediaType}

@router.get('/sizeuom')
async def get_sizeuom():
    return {sizeuom.value for sizeuom in SizeUOM}

@router.get('/logtype')
async def get_logtype():
    return {logtype.value for logtype in LogType}

@router.get('/denloguom')
async def get_denloguom():
    return {denloguom.value for denloguom in DENLogUOM}

@router.get('/porloguom')
async def get_porloguom():
    return {porloguom.value for porloguom in PORLogUOM}





