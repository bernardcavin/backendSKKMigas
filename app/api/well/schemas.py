from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from datetime import date

from app.api.well.models import *
from app.core.constants import UnitType


class WellBase(BaseModel):
    
    unit_type: UnitType

    uwi: Optional[str]
    area_id:Optional[str]
    field_id: Optional[str]
    well_name: Optional[str]
    alias_long_name: Optional[str]

    well_type: Optional[WellType]
    well_status: Optional[WellStatus]
    well_profile_type: Optional[WellProfileType]
    well_directional_type: Optional[WellDirectionalType]
    hydrocarbon_target: Optional[HydrocarbonTarget]
    environment_type: Optional[EnvironmentType]

    surface_longitude: Optional[float]
    surface_latitude: Optional[float]
    bottom_hole_longitude: Optional[float]
    bottom_hole_latitude: Optional[float]
    maximum_inclination: Optional[float]
    azimuth: Optional[float]
    line_name: Optional[str]
    spud_date: Optional[date]
    final_drill_date: Optional[date]
    completion_date: Optional[date]
    rotary_table_elev: Optional[float]
    kb_elev: Optional[float]
    derrick_floor_elev: Optional[float]
    ground_elev: Optional[float]
    mean_sea_level: Optional[float]
    depth_datum: Optional[DepthDatum]
    kick_off_point: Optional[float]
    maximum_tvd: Optional[float]
    final_md: Optional[float]
    remark: Optional[str]

    class Config:
        from_attributes = True

class WellNameResponse(BaseModel):
    well_name: Optional[str]

    class Config:
        from_attributes = True

class WellDocumentBase(BaseModel):
    
    file_id: str
    
    document_type: WellDocumentType
    remark: Optional[str]
    
    class Meta:
        orm_model = WellDocument

class WellDigitalDataBase(BaseModel):
    
    file_id: Optional[str]
    data_format: Optional[DataFormat]

class WellLogBase(WellDigitalDataBase):
    class Meta:
        orm_model = WellLog

class WellTrajectoryBase(WellDigitalDataBase):
    class Meta:
        orm_model = WellTrajectory

class WellPPFGBase(WellDigitalDataBase):
    class Meta:
        orm_model = WellPPFG

class WellDrillingParameterBase(WellDigitalDataBase):
    class Meta:
        orm_model = WellDrillingParameter

class WellSummaryBase(BaseModel):
    
    unit_type: UnitType
    
    depth_datum: Optional[DepthDatum]
    depth: Optional[float]
    hole_diameter: Optional[float]
    bit: Optional[str]
    casing_outer_diameter: Optional[float]
    logging: Optional[str]
    mud_program: Optional[str]
    cementing_program: Optional[str]
    bottom_hole_temperature: Optional[float]
    rate_of_penetration: Optional[float]
    remarks: Optional[str]
    
    class Meta:
        orm_model = WellSummary
    
    class Config:
        from_attributes = True

class WellTestBase(BaseModel):
    
    unit_type: UnitType
    
    depth_datum: Optional[DepthDatum]
    zone_name: Optional[str]
    zone_top_depth: Optional[float]
    zone_bottom_depth: Optional[float]
    
    class Meta:
        orm_model = WellTest

    class Config:
        from_attributes = True

class WellCasingBase(BaseModel):
    
    unit_type: UnitType
    
    depth_datum: Optional[DepthDatum]
    
    depth: Optional[float]
    
    length: Optional[float]
    
    hole_diameter: Optional[float]
    
    casing_outer_diameter: Optional[float]
    
    casing_inner_diameter: Optional[float]
    
    casing_grade: Optional[str]
    
    casing_weight: Optional[float]
    
    connection: Optional[str]
    
    description: Optional[str]
    
    class Meta:
        orm_model = WellCasing

    class Config:
        from_attributes = True

class WellStratigraphyBase(BaseModel):
    
    unit_type: UnitType
    
    depth_datum: Optional[DepthDatum]
    
    depth: Optional[float]
    
    stratigraphy_id: str
    
    class Meta:
        orm_model = WellStratigraphy

    class Config:
        from_attributes = True

class CreatePlanWell(WellBase):
    
    well_documents: Optional[List[WellDocumentBase]] = None
    well_summary: Optional[List[WellSummaryBase]] = None
    well_test: Optional[List[WellTestBase]] = None
    well_trajectory: Optional[WellTrajectoryBase] = None
    well_ppfg: Optional[WellPPFGBase] = None
    well_logs: Optional[List[WellLogBase]] = None
    well_drilling_parameter: Optional[WellDrillingParameterBase] = None
    well_casing: Optional[List[WellCasingBase]] = None
    well_stratigraphy: Optional[List[WellStratigraphyBase]] = None
    
    class Meta:
        orm_model = PlanWell

    class Config:
        from_attributes = True

class CreateActualWell(WellBase):
    
    well_documents: Optional[List[WellDocumentBase]] = None
    well_summary: Optional[List[WellSummaryBase]] = None
    well_test: Optional[List[WellTestBase]] = None
    well_trajectory: Optional[WellTrajectoryBase] = None
    well_ppfg: Optional[WellPPFGBase] = None
    well_logs: Optional[List[WellLogBase]] = None
    well_drilling_parameter: Optional[WellDrillingParameterBase] = None
    well_casing: Optional[List[WellCasingBase]] = None
    well_stratigraphy: Optional[List[WellStratigraphyBase]] = None
    
    class Meta:
        orm_model = ActualWell
    
    class Config:
        from_attributes = True


