from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, JSON, Enum, Text, Boolean
from enum import Enum as PyEnum
from app.database import Base

class TahapanBase(Base):
    __abstract__ = True
    
    @declared_attr
    def pekerjaan_id(cls):
        return Column(String, ForeignKey('pekerjaan.id'))
    
    @declared_attr
    def pekerjaan(cls):
        return relationship("Pekerjaan", foreign_keys=[cls.pekerjaan_id])
    
    @declared_attr
    def kendala_id(cls):
        return Column(String, ForeignKey('kendala.id'))
    
    @declared_attr
    def kendala(cls):
        return relationship("Kendala", foreign_keys=[cls.kendala_id])
    
    @declared_attr
    def pekerjaan_id(cls):
        return Column(String, ForeignKey('pekerjaan.id'))
    
    @declared_attr
    def pekerjaan(cls):
        return relationship("Pekerjaan", foreign_keys=[cls.pekerjaan_id])
    
    @declared_attr
    def created_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def last_edited_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])
    
    @declared_attr
    def last_edited_by(cls):
        return relationship("User", foreign_keys=[cls.last_edited_by_id])

class KategoriKendala(PyEnum):
    RINGAN = 'RINGAN'
    SEDANG = 'SEDANG'
    BERAT = 'BERAT'

class Kendala(Base):
    
    __tablename__ = 'kendala'
    
    id = Column(String, primary_key=True)
    waktu = Column(DateTime)
    kategori = Column(Enum(KategoriKendala))
    deskripsi = Column(Text)
    
    selesai = Column(Boolean)
    waktu_selesai = Column(DateTime)

class StatusPengajuan(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class Pengajuan(TahapanBase):

    __tablename__ = 'pengajuan'

    id = Column(String, primary_key=True)
    
    tanggal_diajukan = Column(DateTime)
    tanggal_ditolak = Column(DateTime)
    tanggal_disetujui = Column(DateTime)
    
    status = Column(Enum(StatusPengajuan))

class StatusOperasi(PyEnum):
    BEROPERASI = 'BEROPERASI'
    TERKENDALA = 'TERKENDALA'
    SELESAI = 'SELESAI'

class Operasi(TahapanBase):

    __tablename__ = 'operasi'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusPPP(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class PPP(TahapanBase):

    __tablename__ = 'ppp'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class StatusCloseOut(PyEnum):
    DIAJUKAN = 'DIAJUKAN'
    DITERIMA = 'DITERIMA'
    DITOLAK = 'DITOLAK'

class CloseOut(TahapanBase):

    __tablename__ = 'closeout'

    id = Column(String, primary_key=True)
    
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    
    status = Column(Enum(StatusOperasi))

class TipePekerjaan(PyEnum):
    EKSPLORASI = 'EKSPLORASI'
    EKSPLOITASI = 'EKSPLOITASI'
    WORKOVER = 'WORKOVER'
    WELLSERVICE = 'WELSERVICE'

class DepthPath(PyEnum):
    
    TVD = 'TVD'
    TVDSS = 'TVDSS'
    MD = 'MD'

class DepthReferencePoint(PyEnum):
    
    GL = 'GL'
    KB = 'KB'
    RT = 'RT'


class Pekerjaan(Base):

    __tablename__ = 'pekerjaan'

    id = Column(String, primary_key=True)
    
    #well_id = Column(String(64), ForeignKey('wells.id'))
    #well = relationship('Well', back_populates='pekerjaan')
    
    kkks = Column(String(64))
    lapangan = Column(String(32))
    wilayah_kerja = Column(String(32))
    tipe_kontrak = Column(String(32))
    tipe_pekerjaan = Column(Enum(TipePekerjaan))
    no_afe = Column(String(32))
    tahun_wpnb = Column(Integer)
    status = Column(String(32))
    
    #plan
    plan_mulai = Column(DateTime)
    plan_selesai = Column(DateTime)
    plan_budget = Column(Numeric(precision=10, scale=2))
    plan_schedule = Column(JSON)

    log_pekerjaan = relationship('LogPekerjaan', back_populates='pekerjaan')
    
    date_created = Column(DateTime)
    last_edited = Column(DateTime)

    created_by_id = Column(Integer,ForeignKey('users.id'))
    last_edited_by_id = Column(Integer, ForeignKey('users.id'))
    last_edited_by = relationship("User", foreign_keys=[last_edited_by_id])
    last_edited_by = relationship("User", foreign_keys=[created_by_id])
    
    __mapper_args__ = {
        'polymorphic_identity': 'pekerjaan',
        'polymorphic_on': tipe_pekerjaan
    }

class LogPekerjaan(Base):
    
    __tablename__ = 'log_pekerjaan'
    
    id = Column(String, primary_key=True)

    waktu = Column(DateTime)
    kedalaman = Column(Numeric)
    depth_path = Column(Enum(DepthPath))
    reference_point = Column(Enum(DepthReferencePoint))
    daily_cost = Column(Numeric(precision=10, scale=2))
    
    summary = Column(Text)
    current_operations = Column(Text)
    next_operations = Column(Text)
    
    pekerjaan_id = Column(String, ForeignKey('pekerjaan.id'))
    pekerjaan = relationship('Pekerjaan', back_populates='log_pekerjaan')


class Eksplorasi(Pekerjaan):
    __mapper_args__ = {
        'polymorphic_identity': TipePekerjaan.EKSPLORASI
    }

class Eksploitasi(Pekerjaan):
    __mapper_args__ = {
        'polymorphic_identity': TipePekerjaan.EKSPLOITASI
    }

class Workover(Pekerjaan):
    __mapper_args__ = {
        'polymorphic_identity': TipePekerjaan.WORKOVER
    }

class WellService(Pekerjaan):
    __mapper_args__ = {
        'polymorphic_identity': TipePekerjaan.WELLSERVICE
    }


