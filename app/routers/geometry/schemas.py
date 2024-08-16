
from pydantic import BaseModel
from app.routers.geometry.models import *
from typing import List

class CreateFieldSchema(BaseModel):

    field_name: str
    area_id: str
    geojson: str

class CreateStratUnitSchema(Base):
    
    area_id: str
    
    strat_unit_name: str
    strat_type: StratType
    strat_unit_type: StratUnitType
    strat_petroleum_system: PetroleumSystem
    
    remark: str

class CreateAreaSchema(BaseModel):
    
    label: str
    area_name: str
    area_phase: AreaPhase
    area_type: AreaType
    area_position: AreaPosition
    area_production_status: AreaProductionStatus
    area_region: AreaRegion
    geojson: str
    
class GetFieldSchema(CreateFieldSchema):
    id: str

class GetStratUnitSchema(CreateAreaSchema):
    id: str
    
class GetAreaSchema(CreateAreaSchema):
    
    id: str
    fields: List[GetFieldSchema]
    strat_units: List[GetStratUnitSchema]

