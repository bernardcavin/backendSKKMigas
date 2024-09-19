
from pydantic import BaseModel
from app.api.spatial.models import *
from typing import List

class CreateFieldSchema(BaseModel):

    name: str
    area_id: str
    geojson: str

class CreateStratUnitSchema(BaseModel):
    
    area_id: str
    
    strat_unit_name: str
    strat_type: StratType
    strat_unit_type: StratUnitType
    strat_petroleum_system: PetroleumSystem
    
    remark: str

class CreateAreaSchema(BaseModel):
    
    label: str
    name: str
    phase: AreaPhase
    type: AreaType
    position: AreaPosition
    production_status: AreaProductionStatus
    region: AreaRegion
    geojson: str
    
class GetFieldSchema(CreateFieldSchema):
    id: str

class GetStratUnitSchema(CreateStratUnitSchema):
    id: str
    
class GetAreaSchema(CreateAreaSchema):
    
    id: str
    fields: List[GetFieldSchema]
    strat_units: List[GetStratUnitSchema]

class AreaResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class LapanganResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class WellInstanceResponse(BaseModel):
    id: str
    well_name: str

    class Config:
        from_attributes = True

class StratUnitResponse(BaseModel):
    id: str
    strat_unit_info: str

