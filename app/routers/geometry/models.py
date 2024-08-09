from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, JSON, Enum
from enum import Enum as PyEnum
from app.database import Base

class FaseWK(PyEnum):
    EKSPLORASI = "EKSPLORASI"
    EKSPLOITASI = "EKSPLOITASI"

class JenisWK(PyEnum):
    KONVENSIONAL = "KONVENSIONAL"
    NONKONVENSIONAL = "NON-KONVENSIONAL"

class LokasiWK(PyEnum):
    ONSHORE = "ONSHORE"
    OFFSHORE = "OFFSHORE"
    ONSHORE_AND_OFFSHORE = "ONSHORE AND OFFSHORE"

class ProduksiWK(PyEnum):
    NONPRODUKSI = 'NON-PRODUKSI'
    PENGEMBANGAN = 'PENGEMBANGAN'
    PRODUKSI = 'PRODUKSI'
    OFF = 'OFF NON-PRODUKSI'

class RegionWK(PyEnum):
    REGION_I = 'REGION I'
    REGION_II = 'REGION II'
    REGION_III = 'REGION III'
    REGION_IV = 'REGION IV'
    REGION_V = 'REGION V'
    REGION_VI = 'REGION VI'

class WilayahKerja(Base):
    
    __tablename__ = 'wilayah_kerja'

    id = Column(String, primary_key=True, index=True)
    label = Column(String, unique=True)
    nama_wk = Column(String, unique=True, index=True)
    fase = Column(Enum(FaseWK))
    jenis = Column(Enum(JenisWK))
    lokasi = Column(Enum(LokasiWK))
    produksi = Column(Enum(ProduksiWK))
    region = Column(Enum(RegionWK))
    fields = relationship("Field", back_populates="wilayah_kerja")
    geojson = Column(JSON)

class Field(Base):   

    __tablename__ = 'field'
    
    id = Column(String, primary_key=True, index=True)
    nama_field = Column(String)
    wilayah_kerja_id = Column(String, ForeignKey('wilayah_kerja.id'))
    wilayah_kerja = relationship("WilayahKerja", back_populates="fields")
    geojson = Column(JSON)
    