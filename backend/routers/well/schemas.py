from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime
from uuid import uuid4

from backend.routers.well.models import *

class WellBase(BaseModel):
    
    uwi: Optional[str]
    field_id: Optional[str]
    area_id: Optional[str]
    kkks_id: Optional[str]
    data_phase: Optional[DataPhase]

    well_name: Optional[str]
    alias_long_name: Optional[str]

    well_type: Optional[WellType]
    well_status: Optional[WellStatus]
    well_profile_type: Optional[WellProfileType]
    hydrocarbon_target: Optional[HydrocarbonTarget]
    environment_type: Optional[EnvironmentType]

    surface_longitude: Optional[float]
    surface_latitude: Optional[float]
    bottom_hole_longitude: Optional[float]
    bottom_hole_latitude: Optional[float]
    maximum_inclination: Optional[float]
    azimuth: Optional[float]

    line_name: Optional[str]

    spud_date: Optional[datetime]
    final_drill_date: Optional[datetime]
    completion_date: Optional[datetime]

    rotary_table_elev: Optional[float]
    rotary_table_elev_uom: Optional[DepthUOM]

    kb_elev: Optional[float]
    kb_elev_uom: Optional[DepthUOM]

    derrick_floor_elev: Optional[float]
    derrick_floor_elev_uom: Optional[DepthUOM]

    ground_elev: Optional[float]
    ground_elev_uom: Optional[DepthUOM]

    mean_sea_level: Optional[float]
    mean_sea_level_uom: Optional[DepthUOM]

    depth_datum: Optional[DepthDatum]
    kick_off_point: Optional[float]
    kick_off_point_uom: Optional[DepthUOM]

    maximum_tvd: Optional[float]
    maximum_tvd_uom: Optional[DepthUOM]

    final_md: Optional[float]
    final_md_uom: Optional[DepthUOM]

    remark: Optional[str]

class WellDocumentBase(BaseModel):
    
    file_id: Optional[str]
    
    title: Optional[str]
    media_type: Optional[MediaType]
    document_type: Optional[str]
    remark: Optional[str]
    
    class Meta:
        orm_model = WellDocument

class WellDigitalDataBase(BaseModel):
    
    file_id: Optional[str]
    data_format: Optional[DataFormat]
    data_class: Optional[DataClass]

class WellLogBase(WellDigitalDataBase):
    data_class: DataClass = DataClass.WELL_LOG
    class Meta:
        orm_model = WellLog

class WellTrajectoryBase(WellDigitalDataBase):
    data_class: DataClass = DataClass.TRAJECTORY
    class Meta:
        orm_model = WellTrajectory

class WellPPFGBase(WellDigitalDataBase):
    data_class: DataClass = DataClass.PPFG
    class Meta:
        orm_model = WellPPFG

class WellDrillingParameterBase(WellDigitalDataBase):
    data_class: DataClass = DataClass.DRILLING_PARAMETER
    class Meta:
        orm_model = WellDrillingParameter

class WellSummaryBase(BaseModel):
    
    depth_datum: Optional[DepthDatum]
    depth: Optional[float]
    depth_uom: Optional[DepthUOM]
    hole_diameter: Optional[float]
    hole_diameter_uom: Optional[DiameterUOM]
    bit: Optional[str]
    casing_outer_diameter: Optional[float]
    casing_outer_diameter_uom: Optional[DiameterUOM]
    logging: Optional[str]
    mud_program: Optional[str]
    cementing_program: Optional[str]
    bottom_hole_temperature: Optional[float]
    bottom_hole_temperature_uom: Optional[TemperatureUOM]
    rate_of_penetration: Optional[float]
    remarks: Optional[str]
    
    class Meta:
        orm_model = WellSummary

class WellTestBase(BaseModel):
    
    depth_datum: Optional[DepthDatum]
    zone_name: Optional[str]
    zone_top_depth: Optional[float]
    zone_bottom_depth: Optional[float]
    depth_uom: Optional[DepthUOM]
    
    class Meta:
        orm_model = WellTest

class WellCasingBase(BaseModel):
    
    depth_datum: Optional[DepthDatum]
    
    depth: Optional[float]
    depth_uom: Optional[DepthUOM]
    
    length: Optional[float]
    length_uom: Optional[DepthUOM]
    
    hole_diameter: Optional[float]
    hole_diameter_uom: Optional[DiameterUOM]
    
    casing_outer_diameter: Optional[float]
    casing_outer_diameter_uom: Optional[DiameterUOM]
    
    casing_inner_diameter: Optional[float]
    casing_inner_diameter_uom: Optional[DiameterUOM]
    
    casing_grade: Optional[str]
    
    casing_weight: Optional[float]
    casing_weight_uom: Optional[WeightUOM]
    
    connection: Optional[str]
    
    description: Optional[str]
    
    class Meta:
        orm_model = WellCasing

class WellStratigraphyBase(BaseModel):
    
    depth_datum: Optional[DepthDatum]
    
    depth: Optional[float]
    depth_uom: Optional[DepthUOM]
    
    stratigraphy_id: str
    
    class Meta:
        orm_model = WellStratigraphy

class CreateWell(WellBase):
    
    well_documents: Optional[List[WellDocumentBase]]
    well_summary: Optional[List[WellSummaryBase]]
    well_test: Optional[List[WellTestBase]]
    well_trajectories: Optional[List[WellTrajectoryBase]]
    well_ppfgs: Optional[List[WellPPFGBase]]
    well_logs: Optional[List[WellLogBase]]
    well_drilling_parameters: Optional[List[WellDrillingParameterBase]]
    well_casing: Optional[List[WellCasingBase]]
    well_stratigraphy: Optional[List[WellStratigraphyBase]]
    
    class Meta:
        orm_model = Well