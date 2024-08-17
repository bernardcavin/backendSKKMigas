from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.routers.well.models import *
from app.routers.well.schemas import *
from app.routers.auth.schemas import GetUser

from typing import Union
from datetime import datetime


def create_well(db: Session, well: CreateWell, data_phase: DataPhase, user: GetUser) -> Well:
    
    db_well_plan = Well(

        date_created=datetime.now(),
        created_by_id=user.id,

        uwi=well.uwi,
        field_id=well.field_id,
        
        # Basic Information
        well_name=well.well_name,
        alias_long_name=well.alias_long_name,
        
        # Well Status and Classification
        well_type=well.well_type,
        well_class=well.well_class,
        well_status=well.well_status,
        profile_type=well.profile_type,
        environment_type=well.environment_type,
        
        # Coordinates
        surface_longitude=well.surface_longitude,
        surface_latitude=well.surface_latitude,
        bottom_hole_longitude=well.bottom_hole_longitude,
        bottom_hole_latitude=well.bottom_hole_latitude,
        
        # Seismic Information
        line_name=well.line_name,
        
        # Key Dates
        spud_date=well.spud_date,
        final_drill_date=well.final_drill_date,
        completion_date=well.completion_date,
        
        # Elevations
        rotary_table_elev=well.rotary_table_elev,
        rotary_table_elev_ouom=well.rotary_table_elev_ouom,
        
        kb_elev=well.kb_elev,
        kb_elev_ouom=well.kb_elev_ouom,
        
        derrick_floor_elev=well.derrick_floor_elev,
        derrick_floor_elev_ouom=well.derrick_floor_elev_ouom,
        
        ground_elev=well.ground_elev,
        ground_elev_ouom=well.ground_elev_ouom,
        
        mean_sea_level=well.mean_sea_level,
        mean_sea_level_ouom=well.mean_sea_level_ouom,
        
        # Depths
        depth_datum=well.depth_datum,
        
        drill_td=well.drill_td,
        drill_td_ouom=well.drill_td_ouom,
        
        log_td=well.log_td,
        log_td_ouom=well.log_td_ouom,
        
        max_tvd=well.max_tvd,
        max_tvd_ouom=well.max_tvd_ouom,
        
        projected_depth=well.projected_depth,
        projected_depth_ouom=well.projected_depth_ouom,
        
        final_td=well.final_td,
        final_td_ouom=well.final_td_ouom,

        remark=well.remark,
        
        data_phase=data_phase
    )
    
    db.add(db_well_plan)
    db.commit()

    well_id = db_well_plan.id

    for document in well.documents:
        db_document = WellDocument(
            well_id=well_id,
            **document.model_dump()
        )
        db.add(db_document)

    for well_log_document in well.well_log_documents:
        db_well_log_document = WellLogDocument(
            well_id=well_id,
            **well_log_document.model_dump()
        )
        db.add(db_well_log_document)

    for well_sample in well.well_samples:
        db_well_sample = WellSample(
            well_id=well_id,
            **well_sample.model_dump()
        )
        db.add(db_well_sample)

    for well_core_sample in well.well_core_samples:
        db_well_core_sample = WellCoreSample(
            well_id=well_id,
            **well_core_sample.model_dump()
        )
        db.add(db_well_core_sample)

    for well_casing in well.well_casing:
        db_well_casing = WellCasing(
            well_id=well_id,
            **well_casing.model_dump()
        )
        db.add(db_well_casing)

    for well_trajectory in well.well_trajectory:
        db_well_trajectory = WellTrajectory(
            well_id=well_id,
            **well_trajectory.model_dump()
        )
        db.add(db_well_trajectory)

    for well_ppfg in well.well_ppfg:
        db_well_ppfg = PorePressureFractureGradient(
            well_id=well_id,
            **well_ppfg.model_dump()
        )
        db.add(db_well_ppfg)

    for well_log in well.well_logs:
        db_well_log = WellLog(
            well_id=well_id,
            **well_log.model_dump()
        )
        db.add(db_well_log)

    for drilling_parameter in well.well_drilling_parameters:
        db_drilling_parameter = DrillingParameter(
            well_id=well_id,
            **drilling_parameter.model_dump()
        )
        db.add(db_drilling_parameter)

    for well_strat in well.well_strat:
        db_well_strat = WellStrat(
            well_id=well_id,
            **well_strat.model_dump()
        )
        db.add(db_well_strat)

    db.commit()
    db.refresh(db_well_plan)
    return db_well_plan

