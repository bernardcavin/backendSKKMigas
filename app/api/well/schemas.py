from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.api.well.models import *
from app.core.constants import UnitType

class WellMandatoryBase(BaseModel):
    
    unit_type: UnitType
    well_type: WellType
    well_profile_type: WellProfileType
    well_directional_type: WellDirectionalType
    hydrocarbon_target: Optional[HydrocarbonTarget]
    environment_type: EnvironmentType

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

    class Config:
        from_attributes = True

class WellBase(WellMandatoryBase):
    
    uwi: Optional[str]
    well_name: str
    alias_long_name: Optional[str]


class WellDocumentBase(BaseModel):
    
    file_id: str
    
    document_type: WellDocumentType
    remark: Optional[str]
    
    class Meta:
        orm_model = WellDocument

    class Config:
        from_attributes = True

class WellDigitalDataBase(BaseModel):
    
    file_id: Optional[str]
    
    class Config:
        from_attributes = True

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
    
    section_name: str
    
    depth_datum: Optional[DepthDatum]
    top_depth: Optional[float]
    bottom_depth: Optional[float]
    hole_diameter: Optional[float]
    bit: Optional[str]
    casing_outer_diameter: Optional[float]
    logging: Optional[str]
    
    #mud program
    mud_type: WellSummaryMudType
    mud_weight: Optional[float]
    mud_viscosity: Optional[float]
    mud_ph_level: Optional[float]
    
    #cementing program
    slurry_volume: Optional[float]
    slurry_mix: Optional[float]
    
    bottom_hole_temperature: Optional[float]
    rate_of_penetration: Optional[float]
    
    rate_of_penetration: Optional[float]
    weight_on_bit: Optional[float]
    rotary_speed: Optional[float]
    
    remarks: Optional[str]
    
    class Meta:
        orm_model = WellSummary
    
    class Config:
        from_attributes = True

class WellTestBase(BaseModel):
    
    unit_type: UnitType
    
    depth_datum: Optional[DepthDatum]
    zone_name: Optional[str]
    top_depth: Optional[float]
    bottom_depth: Optional[float]
    
    class Meta:
        orm_model = WellTest

    class Config:
        from_attributes = True

class WellCasingBase(BaseModel):
    
    unit_type: UnitType
    
    casing_type: CasingType
    
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
    
    depth_datum: DepthDatum
    
    top_depth: float
    bottom_depth: float
    
    formation_name: str
    lithology: str
    
    class Meta:
        orm_model = WellStratigraphy

    class Config:
        from_attributes = True

class WellSchematicBase(BaseModel):

    file_id: str

    class Meta:
        orm_model = WellSchematic
    
    class Config:
        from_attributes = True

class WellBaseWithNests(WellBase):
    
    well_summary: Optional[List[WellSummaryBase]] = None
    well_trajectory: Optional[WellTrajectoryBase] = None
    well_ppfg: Optional[WellPPFGBase] = None
    well_casing: Optional[List[WellCasingBase]] = None
    well_schematic: Optional[WellSchematicBase] = None
    well_stratigraphy: Optional[List[WellStratigraphyBase]] = None

class WellMandatoryBaseWithNests(WellMandatoryBase):
    well_summary: Optional[List[WellSummaryBase]] = None
    well_trajectory: Optional[WellTrajectoryBase] = None
    well_ppfg: Optional[WellPPFGBase] = None
    well_casing: Optional[List[WellCasingBase]] = None
    well_schematic: Optional[WellSchematicBase] = None
    well_stratigraphy: Optional[List[WellStratigraphyBase]] = None

class CreatePlanWell(WellBaseWithNests):
    
    well_test: Optional[List[WellTestBase]] = None

    class Meta:
        orm_model = PlanWell

    class Config:
        from_attributes = True

class CreateDummyPlanWell(CreatePlanWell):
    
    area_id: str
    field_id: str
    kkks_id: str

    class Config:
        from_attributes = True

class ActualWellBase(WellBaseWithNests):
    well_documents: Optional[List[WellDocumentBase]] = None
    well_logs: Optional[List[WellLogBase]] = None
    well_drilling_parameter: Optional[WellDrillingParameterBase] = None

    class Meta:
        orm_model = ActualWell
    
    class Config:
        from_attributes = True


class UpdateActualWell(WellMandatoryBaseWithNests):
    well_documents: Optional[List[WellDocumentBase]] = None
    well_logs: Optional[List[WellLogBase]] = None
    well_drilling_parameter: Optional[WellDrillingParameterBase] = None

    # well_status: Optional[WellStatus]
    # remark: Optional[str]

    class Meta:
        orm_model = ActualWell
    
    class Config:
        from_attributes = True

class CreateActualWell(ActualWellBase):
    
    area_id: str
    field_id: str
    kkks_id: str

class CreateExistingWell(ActualWellBase):
    area_id: str
    field_id: str
    
    
    well_status: Optional[WellStatus]
    remark: Optional[str]

class GetWell(BaseModel):
    well_name: str
    area:str
    field: str
    well_status: Optional[str]  # Izinkan None untuk status
    kkks_id: Optional[str]
    class Config:
        from_attributes = True

class ValidateWell(CreateActualWell):
    pass
