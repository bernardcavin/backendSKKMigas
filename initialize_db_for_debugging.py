
from backend.database import engine, Base
from backend.routers.auth.models import *
from backend.routers.job.models import *
from backend.routers.spatial.models import *
from backend.routers.well.models import *
from backend.routers.utils.models import *

Base.metadata.create_all(bind=engine)