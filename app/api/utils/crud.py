from posixpath import sep
from fastapi import UploadFile, HTTPException
import shutil
import os
from datetime import datetime
from app.api.utils.schemas import *
from sqlalchemy.orm import Session
from app.api.auth.schemas import GetUser
from app.api.utils.models import *
from app.api.well.models import *
import pandas as pd
import io

from app.core.config import settings
from uuid import uuid4
import os



def save_upload_file(db: Session, upload_file: UploadFile, user) -> FileInfo:
    
    if os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir, exist_ok=True)
    
    try:
    
        file_id = str(uuid4())
        file_extension = os.path.splitext(upload_file.filename)[1]
        file_location = os.path.join(settings.upload_dir, f'{file_id}{file_extension}')
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload file")

    try:
        db_file = FileDB(
            id=file_id,
            filename=upload_file.filename,
            file_location=file_location,
            file_extension=file_extension,
            uploaded_by_id=user.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    
    except Exception as e:
        print(e)
        os.remove(file_location)
        raise HTTPException(status_code=500, detail="Failed to save file")

    return FileInfo.model_validate(db_file)
    
def save_upload_multiple_files(db: Session, upload_files: List[UploadFile], user) -> List[FileInfo]:

    file_objs = []
    file_locations = []

    if os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir, exist_ok=True)

    for upload_file in upload_files:
        try:
            file_id = str(uuid4())
            file_extension = os.path.splitext(upload_file.filename)[1]
            file_location = os.path.join(settings.upload_dir, f'{file_id}{file_extension}')
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(upload_file.file, file_object)
            file_locations.append(file_location)
            
        except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to upload files")

        try:
            db_file = FileDB(
                id=file_id,
                filename=upload_file.filename,
                file_location=file_location,
                file_extension=file_extension,
                uploaded_by_id=user.id
            )
            file_objs.append(db_file)
        
        except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to save files")

    try:
        db.add_all(file_objs)
        db.commit()
    except Exception as e:
            if file_locations:
                for file_location in file_locations:
                    os.remove(file_location)
            raise HTTPException(status_code=500, detail="Failed to save files")

    return [FileInfo.model_validate(file_obj) for file_obj in file_objs]

def delete_uploaded_file(db: Session, file_id: str):
    file_info = db.query(FileDB).filter(FileDB.id == file_id).first()
    if file_info is None:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(file_info)
    db.commit()

def jsonify_tabular_file(file: UploadFile):

    if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file.file.read(), engine='openpyxl')
    elif file.content_type == 'text/csv':
        df = pd.read_csv(file.file, sep=';')
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    records = df.to_dict(orient = "records")

    return TabularData(headers=df.columns.to_list(), records=records)

def excel_wbs(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = ["event", "start_date", "end_date", "remarks",]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = WorkBreakdownStructure(
            event=row["event"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            remarks=row["remarks"],
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_drillingfluid(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "mud_type", "time", "mw_in", "mw_out", "temp_in", "temp_out", "pres_grad", "visc",
        "pv", "yp", "gels_10_sec", "gels_10_min", "fluid_loss", "ph", "solids", "sand",
        "water", "oil", "hgs", "lgs", "ltlp", "hthp", "cake", "e_stb", "pf", "mf", "pm", "ecd"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = DrillingFluid(
            mud_type=row["mud_type"],
            time=row["time"],
            mw_in=row["mw_in"],
            mw_out=row["mw_out"],
            temp_in=row["temp_in"],
            temp_out=row["temp_out"],
            pres_grad=row["pres_grad"],
            visc=row["visc"],
            pv=row["pv"],
            yp=row["yp"],
            gels_10_sec=row["gels_10_sec"],
            gels_10_min=row["gels_10_min"],
            fluid_loss=row["fluid_loss"],
            ph=row["ph"],
            solids=row["solids"],
            sand=row["sand"],
            water=row["water"],
            oil=row["oil"],
            hgs=row["hgs"],
            lgs=row["lgs"],
            ltlp=row["ltlp"],
            hthp=row["hthp"],
            cake=row["cake"],
            e_stb=row["e_stb"],
            pf=row["pf"],
            mf=row["mf"],
            pm=row["pm"],
            ecd=row["ecd"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_timebreakdown(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "start_time", "end_time", "start_measured_depth", "end_measured_depth", 
        "category", "p", "npt", "code", "operation"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = TimeBreakdown(
            start_time=row["start_time"],
            end_time=row["end_time"],
            start_measured_depth=row["start_measured_depth"],
            end_measured_depth=row["end_measured_depth"],
            category=row["category"],
            p=row["p"],
            npt=row["npt"],
            code=row["code"],
            operation=row["operation"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_mudadditive(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = ["mud_additive_type", "amount"]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = MudAdditive(
            mud_additive_type=row["mud_additive_type"],
            amount=row["amount"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_bulkmaterial(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "material_type", "material_name", "material_uom", "received", 
        "consumed", "returned", "adjust", "ending"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = BulkMaterial(
            material_type=row["material_type"],
            material_name=row["material_name"],
            material_uom=row["material_uom"],
            received=row["received"],
            consumed=row["consumed"],
            returned=row["returned"],
            adjust=row["adjust"],
            ending=row["ending"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_directionalsurvey(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = ["measured_depth", "inclination", "azimuth"]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = DirectionalSurvey(
            measured_depth=row["measured_depth"],
            inclination=row["inclination"],
            azimuth=row["azimuth"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_personnel(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = ["company", "people"]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = Personnel(
            company=row["company"],
            people=row["people"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_pumps(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "slow_speed", "circulate", "strokes", "pressure", 
        "liner_size", "efficiency"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = Pumps(
            slow_speed=row["slow_speed"],  # Pastikan data sesuai dengan enum YesNo
            circulate=row["circulate"],
            strokes=row["strokes"],
            pressure=row["pressure"],
            liner_size=row["liner_size"],
            efficiency=row["efficiency"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_weather(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "temperature_high", "temperature_low", "chill_factor",
        "wind_speed", "wind_direction", "barometric_pressure",
        "wave_height", "wave_current_speed", "road_condition",
        "visibility"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = Weather(
            temperature_high=row["temperature_high"],
            temperature_low=row["temperature_low"],
            chill_factor=row["chill_factor"],
            wind_speed=row["wind_speed"],
            wind_direction=row["wind_direction"],
            barometric_pressure=row["barometric_pressure"],
            wave_height=row["wave_height"],
            wave_current_speed=row["wave_current_speed"],
            road_condition=row["road_condition"],
            visibility=row["visibility"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_well_summary(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "unit_type", "well_id", "depth_datum", "top_depth", "bottom_depth",
        "depth_uom", "hole_diameter", "hole_diameter_uom", "bit",
        "casing_outer_diameter", "casing_outer_diameter_uom", 
        "logging", "mud_program_id", "cementing_program_id",
        "bottom_hole_temperature", "bottom_hole_temperature_uom", 
        "rate_of_penetration", "remarks"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = WellSummary(
            unit_type=row["unit_type"],  # Pastikan data sesuai dengan enum UnitType
            well_id=row.get("well_id"),  # Nullable
            depth_datum=row["depth_datum"],  # Pastikan data sesuai dengan enum DepthDatum
            top_depth=row["top_depth"],
            bottom_depth=row["bottom_depth"],
            depth_uom=row["depth_uom"],
            hole_diameter=row["hole_diameter"],
            hole_diameter_uom=row["hole_diameter_uom"],
            bit=row["bit"],
            casing_outer_diameter=row["casing_outer_diameter"],
            casing_outer_diameter_uom=row["casing_outer_diameter_uom"],
            logging=row["logging"],
            mud_program_id=row.get("mud_program_id"),  # Nullable
            cementing_program_id=row.get("cementing_program_id"),  # Nullable
            bottom_hole_temperature=row["bottom_hole_temperature"],
            bottom_hole_temperature_uom=row["bottom_hole_temperature_uom"],
            rate_of_penetration=row["rate_of_penetration"],
            remarks=row["remarks"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_well_casing(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "well_id", "unit_type", "depth_datum", "depth", "depth_uom",
        "length", "length_uom", "hole_diameter", "hole_diameter_uom",
        "casing_outer_diameter", "casing_outer_diameter_uom",
        "casing_inner_diameter", "casing_inner_diameter_uom",
        "casing_grade", "casing_weight", "casing_weight_uom",
        "connection", "description"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = WellCasing(
            well_id=row.get("well_id"),  # Nullable
            unit_type=row["unit_type"],  # Pastikan data sesuai dengan enum UnitType
            depth_datum=row["depth_datum"],  # Pastikan data sesuai dengan enum DepthDatum
            depth=row["depth"],
            depth_uom=row["depth_uom"],
            length=row["length"],
            length_uom=row["length_uom"],
            hole_diameter=row["hole_diameter"],
            hole_diameter_uom=row["hole_diameter_uom"],
            casing_outer_diameter=row["casing_outer_diameter"],
            casing_outer_diameter_uom=row["casing_outer_diameter_uom"],
            casing_inner_diameter=row["casing_inner_diameter"],
            casing_inner_diameter_uom=row["casing_inner_diameter_uom"],
            casing_grade=row["casing_grade"],
            casing_weight=row["casing_weight"],
            casing_weight_uom=row["casing_weight_uom"],
            connection=row["connection"],
            description=row["description"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_well_stratigraphy(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "unit_type", "well_id", "depth_datum", "top_depth", "bottom_depth",
        "depth_uom", "formation_name", "lithology"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = WellStratigraphy(
            unit_type=row["unit_type"],  # Pastikan data sesuai dengan enum UnitType
            well_id=row.get("well_id"),  # Nullable
            depth_datum=row["depth_datum"],  # Pastikan data sesuai dengan enum DepthDatum
            top_depth=row["top_depth"],
            bottom_depth=row["bottom_depth"],
            depth_uom=row["depth_uom"],
            formation_name=row["formation_name"],
            lithology=row["lithology"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_well_test(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "unit_type", "well_id", "depth_datum", "zone_name", 
        "top_depth", "bottom_depth", "depth_uom"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        data = WellTest(
            unit_type=row["unit_type"],  # Pastikan data sesuai dengan enum UnitType
            well_id=row.get("well_id"),  # Nullable
            depth_datum=row["depth_datum"],  # Pastikan data sesuai dengan enum DepthDatum
            zone_name=row["zone_name"],
            top_depth=row["top_depth"],
            bottom_depth=row["bottom_depth"],
            depth_uom=row["depth_uom"]  # Dapat disesuaikan jika diperlukan
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_job_hazard(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "job_instance_id", "hazard_type", "hazard_description", 
        "severity", "mitigation", "remark"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        # Pastikan untuk memvalidasi nilai enum jika diperlukan
        hazard_type_value = row["hazard_type"]  # Gantilah ini dengan validasi jika perlu
        severity_value = row["severity"]  # Gantilah ini dengan validasi jika perlu

        data = JobHazard(
            job_instance_id=row["job_instance_id"],
            hazard_type=hazard_type_value,  # Pastikan data sesuai dengan enum HazardType
            hazard_description=row["hazard_description"],
            severity=severity_value,  # Pastikan data sesuai dengan enum Severity
            mitigation=row["mitigation"],
            remark=row["remark"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_job_operation_day(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "job_instance_id", "unit_type", "phase", 
        "depth_datum", "depth_in", "depth_out", 
        "operation_days"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        # Validasi nilai enum jika diperlukan
        unit_type_value = row["unit_type"]  # Gantilah ini dengan validasi jika perlu
        depth_datum_value = row["depth_datum"]  # Gantilah ini dengan validasi jika perlu

        data = JobOperationDay(
            job_instance_id=row["job_instance_id"],
            unit_type=unit_type_value,  # Pastikan data sesuai dengan enum UnitType
            phase=row["phase"],
            depth_datum=depth_datum_value,  # Pastikan data sesuai dengan enum DepthDatum
            depth_in=row["depth_in"],
            depth_out=row["depth_out"],
            operation_days=row["operation_days"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}

def excel_job_document(file, db: Session):
    # Periksa apakah file adalah Excel
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="File bukan Excel")

    # Membaca file Excel ke dalam DataFrame
    contents = file.file.read()
    excel_data = pd.read_excel(io.BytesIO(contents))

    # Pastikan header sesuai dengan yang diinginkan
    expected_columns = [
        "job_instance_id", "file_id", 
        "document_type", "remark"
    ]
    if not all(col in excel_data.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Header tidak sesuai")

    # Menyimpan data ke database
    for _, row in excel_data.iterrows():
        # Validasi nilai enum jika diperlukan
        document_type_value = row["document_type"]  # Gantilah ini dengan validasi jika perlu

        data = JobDocument(
            job_instance_id=row["job_instance_id"],
            file_id=row["file_id"],  # Pastikan file_id valid
            document_type=document_type_value,  # Pastikan data sesuai dengan enum JobDocumentType
            remark=row["remark"]
        )
        db.add(data)

    db.commit()
    return {"message": "Data berhasil diunggah dan disimpan ke database"}



