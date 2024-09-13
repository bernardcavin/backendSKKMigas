from pydantic import BaseModel
from app.api.spatial.models import *
from typing import List

class VisualizeCasing(BaseModel):
    
    names: List[str]
    top_depths: List[float]
    bottom_depths: List[float]
    diameters: List[float]