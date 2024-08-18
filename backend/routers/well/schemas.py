from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from backend.routers.well.models import *

class CreateWellDigitalData(BaseModel):

    file_id: str

class CreateWellLog(CreateWellDigitalData):

    pass

class CreateWellTrajectory(CreateWellDigitalData):

    pass

class CreateWellDrillingParameter(CreateWellDigitalData):

    pass

class CreateWellPPFG(CreateWellDigitalData):

    pass

class CreateWellDocument(BaseModel):

    file_id: str

    title: str
    
    media_type: MediaType
    document_type: str
    
    remark: str

class CreateWellCasing(BaseModel):
    casing_type: CasingType
    grade: str
    inside_diameter: float
    inside_diameter_ouom: CasingUOM
    outside_diameter: float
    outside_diameter_ouom: CasingUOM
    base_depth: float
    base_depth_ouom: DepthUOM

class CreateWellStrat(BaseModel):
    strat_unit_id: str
    depth_datum: DepthDatum
    top_depth: float
    bottom_depth: float
    depth_uoum: DepthUOM

class SchemaOutput(BaseModel):
    id: str

class WellBase(BaseModel):
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
    environment_type: EnvironmentType  # EnvironmentType Type (PPDM: ENVIRONMENT_TYPE)
    
    # Coordinates
    surface_longitude: float  # Surface Longitude (PPDM: SURFACE_LONGITUDE)
    surface_latitude: float  # Surface Latitude (PPDM: SURFACE_LATITUDE)
    bottom_hole_longitude: float
    bottom_hole_latitude: float
    maximum_inclination: float #degrees
    maximum_azimuth: float #degrees

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
    
    kick_off_point: float
    kick_off_point_ouom: DepthUOM

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

class CreateWell(WellBase):
       
    well_documents: Optional[List[CreateWellDocument]]
    well_casings: Optional[List[CreateWellCasing]]
    well_trajectories: Optional[List[CreateWellTrajectory]]
    well_ppfgs: Optional[List[CreateWellPPFG]]
    well_logs: Optional[List[CreateWellLog]]
    well_drilling_parameters: Optional[List[CreateWellDrillingParameter]]
    well_strat: Optional[List[CreateWellStrat]]

class CreateWellDirectly(CreateWell):
    field_id: str
    data_phase: DataPhase

class GetWell(WellBase):

    id: str

    well_documents: Optional[List[SchemaOutput]]
    well_casings: Optional[List[SchemaOutput]]
    well_trajectories: Optional[List[SchemaOutput]]
    well_ppfgs: Optional[List[SchemaOutput]]
    well_logs: Optional[List[SchemaOutput]]
    well_drilling_parameters: Optional[List[SchemaOutput]]
    well_strat: Optional[List[SchemaOutput]]
