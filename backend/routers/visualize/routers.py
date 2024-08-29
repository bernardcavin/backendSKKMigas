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
from backend.routers.visualize import schemas
from backend.routers.visualize import utils
import uuid

router = APIRouter(prefix="/visualize", tags=["visualize"])

session_ids = {}

class SessionId:
    
    def __init__(self, session_id: str):
        self.session_id = session_id

    def delete_session_id(self):
        del session_ids[self.session_id]

# @router.get("/well-log/{well_id}")
# @authorize(role=[Role.Admin, Role.KKKS])
# async def create_upload_file(well_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
#     well_data = get_well_data(DataClass.WELL_LOG, db, well_id)
#     img_buf = generate_well_logs(well_data.file)
#     background_tasks.add_task(img_buf.close)
#     headers = {'Content-Disposition': 'inline; filename="out.png"'}
#     return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

def request_visualize_casing(casing: schemas.VisualizeCasing):
    session_id = str(uuid.uuid4())
    session_ids[session_id] = {
        'session_id': SessionId(session_id),
        'schema': casing
    }
    
    return {
        'session_id':session_id,
        'path':f'/visualize/casing-visualization/{session_id}'
    }

@router.post("/visualize-casing")
@authorize(role=[Role.Admin, Role.KKKS])
async def visualize_casing_request(casing: schemas.VisualizeCasing, user: GetUser = Depends(get_current_user)):
    return visualize_casing(casing)

@router.get("/casing-visualization/{session_id}")
@authorize(role=[Role.Admin, Role.KKKS])
async def visualize_casing(session_id: str, background_tasks: BackgroundTasks, user: GetUser = Depends(get_current_user)):
    casing = session_ids[session_id]['schema']
    img_buf = utils.generate_well_casing(
        casing.names, casing.top_depths, casing.bottom_depths, casing.diameters
    )
    background_tasks.add_task(img_buf.close)
    background_tasks.add_task(session_ids[session_id]['session_id'].delete_session_id)
    headers = {'Content-Disposition': 'inline; filename="casing.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

