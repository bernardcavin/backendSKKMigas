import matplotlib
from fastapi import Response, BackgroundTasks, APIRouter, Depends
from app.api.auth.models import Role
from app.api.auth.schemas import GetUser
from app.core.security import authorize, get_current_user
from app.api.visualize import schemas, utils
from app.core.schema_operations import create_api_response
import uuid

matplotlib.use('AGG')

router = APIRouter(prefix="/visualize", tags=["visualize"])

session_ids = {}

class SessionId:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def delete_session_id(self):
        del session_ids[self.session_id]

def request_visualize_casing(casing: schemas.VisualizeCasing):
    session_id = str(uuid.uuid4())
    session_ids[session_id] = {
        'session_id': SessionId(session_id),
        'schema': casing
    }
    return {
        'session_id': session_id,
        'path': f'/visualize/casing-visualization/{session_id}'
    }

@router.post("/visualize-casing")
@authorize(role=[Role.Admin, Role.KKKS])
async def visualize_casing_request(casing: schemas.VisualizeCasing, user = Depends(get_current_user)):
    try:
        response_data = request_visualize_casing(casing)
        return create_api_response(success=True, message="Casing visualization requested successfully", data=response_data)
    except Exception as e:
        return create_api_response(success=False, message="Failed to request casing visualization", status_code=500)

@router.get("/casing-visualization/{session_id}")
@authorize(role=[Role.Admin, Role.KKKS])
async def visualize_casing(session_id: str, background_tasks: BackgroundTasks, user = Depends(get_current_user)):
    if session_id not in session_ids:
        return create_api_response(success=False, message="Invalid session ID", status_code=404)

    try:
        casing = session_ids[session_id]['schema']
        img_buf = utils.generate_well_casing(
            casing.names, casing.top_depths, casing.bottom_depths, casing.diameters
        )
        background_tasks.add_task(img_buf.close)
        background_tasks.add_task(session_ids[session_id]['session_id'].delete_session_id)
        headers = {'Content-Disposition': 'inline; filename="casing.png"'}
        return Response(img_buf.getvalue(), headers=headers, media_type='image/png')
    except Exception as e:
        return create_api_response(success=False, message="Failed to generate casing visualization", status_code=500)

# Uncomment and adjust the following endpoint as needed if you want to use it
# @router.get("/well-log/{well_id}")
# @authorize(role=[Role.Admin, Role.KKKS])
# async def create_upload_file(well_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user = Depends(get_current_user)):
#     try:
#         well_data = get_well_data(DataClass.WELL_LOG, db, well_id)
#         img_buf = generate_well_logs(well_data.file)
#         background_tasks.add_task(img_buf.close)
#         headers = {'Content-Disposition': 'inline; filename="out.png"'}
#         return Response(img_buf.getvalue(), headers=headers, media_type='image/png')
#     except Exception as e:
#         return create_api_response(success=False, message="Failed to generate well log visualization", status_code=500)
