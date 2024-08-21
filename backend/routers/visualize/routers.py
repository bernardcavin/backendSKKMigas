import matplotlib
from backend.routers.visualize.lib.well_logs import generate_well_logs
matplotlib.use('AGG')
from fastapi import Response, BackgroundTasks
from backend.routers.visualize.lib.well_casing import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.routers.auth.models import *
from backend.routers.well.models import DataClass
from backend.routers.utils.crud import *
from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.visualize.crud import get_well_data

router = APIRouter(prefix="/visualize", tags=["visualize"])

@router.get("/well-log/{well_id}")
@authorize(role=[Role.Admin, Role.KKKS])
async def create_upload_file(well_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    well_data = get_well_data(DataClass.WELL_LOG, db, well_id)
    img_buf = generate_well_logs(well_data.file)
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

