from typing import List


from app.api.job.models import *
from app.api.well.schemas import *
from pydantic import ValidationError

from pydantic import BaseModel, field_validator, model_validator, Extra
from typing import Optional, Union
from datetime import datetime, date,time

from .utils import validate_time

class TimeBreakdownBase(BaseModel):
    date: date
    start_time: Union[time, datetime]
    end_time: Union[time, datetime]
    start_measured_depth: float
    end_measured_depth: float
    category: JobCategory
    p: YesNo
    npt: NPT
    code: str
    operation: str
    code: OperationCode

    # class Meta:
    #     orm_model = TimeBreakdown
    
    # @field_validator('start_time', 'end_time')
    # @classmethod
    # def parse_time(cls, v):
    #     validate_time(v)
    #     return v

    @model_validator(mode='before')
    @classmethod
    def end_time_must_be_after_start_time(cls, v):
        
        if not isinstance(v , dict):
            v = v.__dict__
        
        if isinstance(v.get('start_time'), datetime):
            date = v.get('start_time').date()
            v['date'] = date
        else:
            date = datetime.strptime(v.get('date'), "%Y-%m-%d").date()
        
        start = validate_time(date, v.get('start_time'))
        end = validate_time(date, v.get('end_time'))
        
        if start is not None and end <= start:
            raise Exception('end_time must be after start_time')
        
        v['start_time'] = start
        v['end_time'] = end
        
        return v

class TimeBreakdownCreate(TimeBreakdownBase):
    
    class Meta:
        orm_model = TimeBreakdown
    
    class Config:
        from_attributes = True

# class TimeBreakdownInDB(TimeBreakdownBase):
#     class Config:
#         from_attributes = True

class PersonnelBase(BaseModel):
    company: str
    people: int

    # class Meta:
    #     orm_model = Personnel

class PersonnelCreate(PersonnelBase):
    
    class Meta:
        orm_model = Personnel
        
    class Config:
        from_attributes = True

# class PersonnelInDB(PersonnelBase):

#     class Config:
#         from_attributes = True


class IncidentBase(BaseModel):
    date: date
    incidents_time: Union[time, datetime]
    incident: str
    incident_type: str
    comments: Optional[str] = None
    
    # @field_validator('incidents_time')
    # @classmethod
    # def parse_time(cls, v):
    #     return validate_time(v)
    
    @model_validator(mode='before')
    @classmethod
    def incident_time_validation(cls, v):
        
        if not isinstance(v , dict):
            v = v.__dict__
        
        if isinstance(v.get('incidents_time'), datetime):
            date = v.get('incidents_time').date()
            v['date'] = date
        else:
            date = datetime.strptime(v.get('date'), "%Y-%m-%d").date()
        
        incidents_time = validate_time(date, v.get('incidents_time'))
        
        v['incidents_time'] = incidents_time
        
        return v

    # class Meta:
    #     orm_model = Incident

class IncidentCreate(IncidentBase):
    
    class Meta:
        orm_model = Incident
        
    class Config:
        from_attributes = True

# class IncidentInDB(IncidentBase):
#     class Config:
#         from_attributes = True

class BitRecordBase(BaseModel):
    bit_size: float
    bit_number: int
    bit_run: int
    manufacturer: str
    iadc_code: str
    jets: str
    serial: str
    depth_out: float
    depth_in: float
    meterage: float
    bit_hours: float
    nozzels: float
    dull_grade: str

    # class Meta:
    #     orm_model = BitRecord
        
class BitRecordCreate(BitRecordBase):
    class Meta:
        orm_model = BitRecord
    
    class Config:
        from_attributes = True

# class BitRecordInDB(BitRecordBase):
#     pass
#     class Config:
#         from_attributes = True


class BHAComponentBase(BaseModel):
    component: BHAComponentType
    outer_diameter: float
    length: float

    # class Meta:
    #     orm_model = BHAComponent

class BHAComponentCreate(BHAComponentBase):
    
    class Meta:
        orm_model = BHAComponent
    
    class Config:
        from_attributes = True

# class BHAComponentInDB(BHAComponentBase):
#     pass
#     model_config = ConfigDict(from_attributes=True)

class BottomHoleAssemblyBase(BaseModel):

    bha_number: int
    bha_run: int

    # class Meta:
    #     orm_model = BottomHoleAssembly

class BottomHoleAssemblyCreate(BottomHoleAssemblyBase):
    components: List[BHAComponentCreate]
    
    class Meta:
        orm_model = BottomHoleAssembly
    
    class Config:
        from_attributes = True

# class BottomHoleAssemblyInDB(BottomHoleAssemblyBase):
#     components: List[BHAComponentInDB]

#     model_config = ConfigDict(from_attributes=True)

class DrillingFluidBase(BaseModel):
    mud_type: MudType
    date: date
    time: Union[time, datetime]
    mw_in: float
    mw_out: float
    temp_in: float
    temp_out: float
    pres_grad: float
    visc: float
    pv: float
    yp: float
    gels_10_sec: float
    gels_10_min: float
    fluid_loss: float
    ph: float
    solids: float
    sand: float
    water: float
    oil: float
    hgs: float
    lgs: float
    ltlp: float
    hthp: float
    cake: float
    e_stb: float
    pf: float
    mf: float
    pm: float
    ecd: float

    # class Meta:
    #     orm_model = DrillingFluid

    @model_validator(mode='before')
    @classmethod
    def time_validation(cls, v):
        
        if not isinstance(v , dict):
            v = v.__dict__
        
        if isinstance(v.get('time'), datetime):
            date = v.get('time').date()
            v['date'] = date
        else:
            date = datetime.strptime(v.get('date'), "%Y-%m-%d").date()
        
        incidents_time = validate_time(date, v.get('time'))
        
        v['time'] = incidents_time
        
        return v
        
        return v

class DrillingFluidCreate(DrillingFluidBase):
    
    class Meta:
        orm_model = DrillingFluid
    
    class Config:
        from_attributes = True

# class DrillingFluidInDB(DrillingFluidBase):
#     pass
#     model_config = ConfigDict(from_attributes=True)

class MudAdditiveBase(BaseModel):
    mud_additive_type: str
    amount: float

class MudAdditiveCreate(MudAdditiveBase):
    
    class Meta:
        orm_model = MudAdditive
        
    class Config:
        from_attributes = True

# class MudAdditiveInDB(MudAdditiveBase):
#     pass
#     model_config = ConfigDict(from_attributes=True)

class BulkMaterialBase(BaseModel):
    material_type: str
    material_name: str
    material_uom: str
    received: float
    consumed: float
    returned: float
    adjust: float
    ending: float



class BulkMaterialCreate(BulkMaterialBase):
    
    class Meta:
        orm_model = BulkMaterial
        
    class Config:
        from_attributes = True

# class BulkMaterialInDB(BulkMaterialBase):
#     model_config = ConfigDict(from_attributes=True)

class DirectionalSurveyBase(BaseModel):
    measured_depth: float
    inclination: float
    azimuth: float

class DirectionalSurveyCreate(DirectionalSurveyBase):
    
    class Meta:
        orm_model = DirectionalSurvey
    
    class Config:
        from_attributes = True

# class DirectionalSurveyInDB(DirectionalSurveyBase):

#     model_config = ConfigDict(from_attributes=True)

class PumpsBase(BaseModel):
    slow_speed: YesNo
    circulate: float
    strokes: float
    pressure: float
    liner_size: float
    efficiency: float

class PumpsCreate(PumpsBase):
    
    class Meta:
        orm_model = Pumps
    
    class Config:
        from_attributes = True

# class PumpsInDB(PumpsBase):
#     model_config = ConfigDict(from_attributes=True)

class WeatherBase(BaseModel):
    temperature_high: float
    temperature_low: float
    chill_factor: float
    wind_speed: float
    wind_direction: float
    barometric_pressure: float
    wave_height: float
    wave_current_speed: float
    road_condition: str
    visibility: str

class WeatherCreate(WeatherBase):
    
    class Meta:
        orm_model = Weather
    
    class Config:
        from_attributes = True

# class WeatherInDB(WeatherBase):
#     model_config = ConfigDict(from_attributes=True)

class DailyOperationsReportBase(BaseModel):
    
    avg_wob: Optional[float]
    avg_rop: Optional[float]
    avg_rpm: Optional[float]
    torque: Optional[float]
    stand_pipe_pressure: Optional[float]
    flow_rate: Optional[float]
    string_weight: Optional[float]
    rotating_weight: Optional[float]
    total_drilling_time: Optional[float]
    circulating_pressure: Optional[float]
    daily_cost: Optional[float]
    daily_mud_cost: Optional[float]
    day_supervisor: Optional[float]
    night_supervisor: Optional[float]
    engineer: Optional[float]
    geologist: Optional[float]
    day_summary: Optional[str]
    day_forecast: Optional[str]
    last_size: Optional[float]
    set_md: Optional[float]
    next_size: Optional[float]
    next_set_md: Optional[float]
    last_lot_emw: Optional[float]
    tol: Optional[float]
    start_mud_volume: Optional[float]
    lost_surface_mud_volume: Optional[float]
    lost_dh_mud_volume: Optional[float]
    dumped_mud_volume: Optional[float]
    built_mud_volume: Optional[float]
    ending_mud_volume: Optional[float]
    max_gas: Optional[float]
    conn_gas: Optional[float]
    trip_gas: Optional[float]
    back_gas: Optional[float]
    annular_velocity: Optional[float]
    pb: Optional[float]
    sys_hhp: Optional[float]
    hhpb: Optional[float]
    hsi: Optional[float]
    percent_psib: Optional[float]
    jet_velocity: Optional[float]
    impact_force: Optional[float]
    if_area: Optional[float]
    stop_cards: Optional[int]
    lta: Optional[YesNo]
    spill: Optional[YesNo]
    h2s_test: Optional[YesNo]
    hse_mtg: Optional[YesNo]
    kicktrip: Optional[YesNo]
    kickdrill: Optional[YesNo]
    fire: Optional[YesNo]

    personnel: Optional[List[PersonnelCreate]]
    Incidents: Optional[List[IncidentCreate]]
    time_breakdowns: Optional[List[TimeBreakdownCreate]]
    bit_records: Optional[List[BitRecordCreate]]
    bottom_hole_assemblies: Optional[List[BottomHoleAssemblyCreate]]
    drilling_fluids: Optional[List[DrillingFluidCreate]]
    mud_additives: Optional[List[MudAdditiveCreate]]
    bulk_materials: Optional[List[BulkMaterialCreate]]
    directional_surveys: Optional[List[DirectionalSurveyCreate]]
    pumps: Optional[List[PumpsCreate]]
    weather: Optional[WeatherCreate]

    class Meta:
        orm_model = DailyOperationsReport
        
    class Config:
        from_attributes = True

class DailyOperationsReportCreate(DailyOperationsReportBase):
    report_date: date
    # job_id: str


class DailyOperationsReportEdit(DailyOperationsReportBase):
    pass
    # job_id: str


# class DailyOperationsReportUpdate(DailyOperationsReportBase):
    
#     time_breakdowns: List[TimeBreakdownCreate]

# class DailyOperationsReportInDB(DailyOperationsReportBase):
#     id: str
#     job_id: str
#     time_breakdowns: List[TimeBreakdownInDB]
#     personnel: List[PersonnelInDB]
#     Incidents: List[IncidentInDB]
#     bit_records: List[BitRecordInDB]
#     bottom_hole_assemblies: List[BottomHoleAssemblyInDB]
#     drilling_fluids: List[DrillingFluidInDB]
#     mud_additives: List[MudAdditiveInDB]
#     bulk_materials: List[BulkMaterialInDB]
#     directional_surveys: List[DirectionalSurveyInDB]
#     pumps: List[PumpsInDB]
#     weather: WeatherInDB

#     model_config = ConfigDict(from_attributes=True)

# class ReportResponse(BaseModel):
#     data: DailyOperationsReportInDB
#     status: int

