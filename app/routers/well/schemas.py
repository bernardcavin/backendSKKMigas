from typing import Dict, Any, Union, List

from pydantic import BaseModel, condecimal, Json
from datetime import datetime

from app.routers.well.models import *

class CreateWellDocument(BaseModel):
    well_id: str
    title: str
    creator_name: str
    create_date: datetime
    media_type: MediaType
    document_type: str
    item_category: str
    item_sub_category: str
    digital_format: str
    original_file_name: str
    digital_size: float
    digital_size_uom: SizeUOM
    remark: str

class GetWellDocument(CreateWellDocument):
    id: str


class CreateWellLogDocument(BaseModel):
    well_id: str
    logging_company: str
    media_type: MediaType
    log_title: str
    digital_format: str
    report_log_run: str
    trip_date: datetime
    top_depth: float
    top_depth_ouom: DepthUOM
    base_depth: float
    base_depth_ouom: DepthUOM
    original_file_name: str
    digital_size: float
    digital_size_uom: SizeUOM
    remark: str

class GetWellLogDocument(CreateWellLogDocument):
    id: str


class CreateWellSample(BaseModel):
    well_id: str
    sample_type: str
    sample_num: str
    sample_count: int
    top_md: float
    top_md_ouom: DepthUOM
    base_md: float
    base_md_ouom: DepthUOM
    study_type: str
    remark: str

class GetWellSample(CreateWellSample):
    id: str


class CreateWellCoreSample(BaseModel):
    well_id: str
    core_type: str
    sample_num: str
    sample_count: int
    top_depth: float
    top_depth_ouom: DepthUOM
    base_depth: float
    base_depth_ouom: DepthUOM
    portion_volume: float
    portion_volume_ouom: VolumeUOM
    study_type: str
    remark: str

class GetWellCoreSample(CreateWellCoreSample):
    id: str


class CreateWellCasing(BaseModel):
    well_id: str
    casing_type: CasingType
    grade: str
    inside_diameter: float
    inside_diameter_ouom: CasingUOM
    outside_diameter: float
    outside_diameter_ouom: CasingUOM
    base_depth: float
    base_depth_ouom: DepthUOM

class GetWellCasing(CreateWellCasing):
    id: str


class CreateWellTrajectory(BaseModel):
    well_id: str
    measured_depth: float
    true_vertical_depth: float
    true_vertical_depth_sub_sea: float
    inclination: float
    azimuth: float
    latitude: float
    longitude: float

class GetWellTrajectory(CreateWellTrajectory):
    id: str


class CreatePorePressureFractureGradient(BaseModel):
    well_id: str
    depth_datum: DepthDatum
    depth: float
    depth_uoum: DepthUOM
    overburden_stress: float
    pore_pressure: float
    fracture_pressure: float

class GetPorePressureFractureGradient(CreatePorePressureFractureGradient):
    id: str


class CreateWellLog(BaseModel):
    well_id: str
    depth_datum: DepthDatum
    depth: float
    depth_uoum: DepthUOM
    gamma_ray_log_name: str
    gamma_ray_log: float
    gamma_ray_log_ouom: GRLogUOM
    density_log_name: str
    density_log: float
    density_log_ouom: DENLogUOM
    porosity_log_name: str
    porosity_log: float
    porosity_log_ouom: PORLogUOM

class GetWellLog(CreateWellLog):
    id: str


class CreateDrillingParameter(BaseModel):
    well_id: str
    depth_datum: DepthDatum
    depth: float
    depth_uoum: DepthUOM
    rate_of_penetration: float
    weight_on_bit: float
    hookload: float
    top_drive: float
    mud_motor: float
    total_rpm: float
    torque: float
    mud_weight: float

class GetDrillingParameter(CreateDrillingParameter):
    id: str


class CreateWellStrat(BaseModel):
    well_id: str
    strat_unit_id: str
    depth_datum: DepthDatum
    top_depth: float
    bottom_depth: float
    depth_uoum: DepthUOM

class GetWellStrat(CreateWellStrat):
    id: str

class CreateWell(BaseModel):
    
    uwi: str
    field_id: str
        
    # Basic Information
    well_name: str
    alias_long_name: str
        
    # Well Status and Classification
    well_type: WellType
    well_class: WellClass
    well_status: WellStatus
    profile_type: ProfileType
    environment_type: Environment  # Environment Type (PPDM: ENVIRONMENT_TYPE)
    
    # Coordinates
    surface_longitude: float  # Surface Longitude (PPDM: SURFACE_LONGITUDE)
    surface_latitude: float  # Surface Latitude (PPDM: SURFACE_LATITUDE)
    bottom_hole_longitude: float
    bottom_hole_latitude: float
        
    # Seismic Information
    line_name: str  # Line Name (PPDM: LINE_NAME)
    
    # Key Dates
    spud_date: datetime  # Spud Date (PPDM: SPUD_DATE)
    final_drill_date: datetime  # Final Drill Date (PPDM: FINAL_DRILL_DATE)
    completion_date: datetime  # Completion Date (PPDM: COMPLETION_DATE)
    
    # Elevations
    rotary_table_elev: float  # Rotary Table Elevation (PPDM: ROTARY_TABLE_ELEV)
    rotary_table_elev_ouom: DepthUOM  # Rotary Table Elevation ODepthUOM (PPDM: ROTARY_TABLE_ELEV_ODepthUOM)
    
    kb_elev: float  # Kelly Bushing Elevation (PPDM: KB_ELEV)
    kb_elev_ouom: DepthUOM  # Kelly Bushing Elevation ODepthUOM (PPDM: KB_ELEV_ODepthUOM)
    
    derrick_floor_elev: float  # Derrick Floor Elevation (PPDM: DERRICK_FLOOR_ELEV)
    derrick_floor_elev_ouom: DepthUOM  # Derrick Floor Elevation ODepthUOM (PPDM: DERRICK_FLOOR_ELEV_ODepthUOM)
    
    ground_elev: float  # Ground Elevation (PPDM: GROUND_ELEV)
    ground_elev_ouom: DepthUOM # Ground Elevation ODepthUOM (PPDM: GROUND_ELEV_ODepthUOM)
    
    mean_sea_level: float
    mean_sea_level_ouom: DepthDatum
    
    # Depths
    depth_datum: DepthDatum  # Depth Datum (PPDM: DEPTH_DATUM)
    
    drill_td: float  # Drill Total Depth (PPDM: DRILL_TD)
    drill_td_ouom: DepthUOM  # Drill Total Depth ODepthUOM (PPDM: DRILL_TD_ODepthUOM)
    
    log_td: float  # Log Total Depth (PPDM: LOG_TD)
    log_td_ouom: DepthUOM  # Log Total Depth ODepthUOM (PPDM: LOG_TD_ODepthUOM)
    
    max_tvd: float  # Maximum True Vertical Depth (PPDM: MAX_TVD)
    max_tvd_ouom: DepthUOM  # Maximum True Vertical Depth ODepthUOM (PPDM: MAX_TVD_ODepthUOM)
    
    projected_depth: float  # Projected Depth (PPDM: PROJECTED_DEPTH)
    projected_depth_ouom: DepthUOM  # Projected Depth ODepthUOM (PPDM: PROJECTED_DEPTH_ODepthUOM)
    
    final_td: float  # Final Total Depth (PPDM: FINAL_TD)
    final_td_ouom: DepthUOM  # Final Total Depth ODepthUOM (PPDM: FINAL_TD_ODepthUOM)

    remark: str  # Remarks (PPDM: REMARK)
    
    documents: List[GetWellDocument]
    well_log_documents: List[GetWellLogDocument]
    well_samples: List[GetWellSample]
    well_core_samples: List[GetWellCoreSample]
    well_casing: List[GetWellCasing]
    well_trajectory: List[GetWellTrajectory]
    well_ppfg: List[GetPorePressureFractureGradient]
    well_logs: List[GetWellLog]
    well_drilling_parameters: List[GetDrillingParameter]
    well_strat: List[GetWellStrat]

class GetWell(CreateWell):
    id: str