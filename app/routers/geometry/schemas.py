
from pydantic import BaseModel
from app.routers.geometry.models import FaseWK,JenisWK,LokasiWK, ProduksiWK, RegionWK

class WilayahKerjaSchema(BaseModel):
    
    id: str
    label: str
    nama_wk: str
    fase: FaseWK
    jenis: JenisWK
    lokasi: LokasiWK
    produksi: ProduksiWK
    region: RegionWK
    geojson: str
    
class FieldSchema(BaseModel):

    id: str
    nama_field: str
    wilayah_kerja_id: str
    geojson: str
