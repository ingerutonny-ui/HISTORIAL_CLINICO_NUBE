from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True, index=True)
    codigo_paciente = Column(String, unique=True)
    
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")
    antecedentes = relationship("AntecedentesP2", back_populates="paciente")
    habitos_riesgos = relationship("HabitosRiesgosP3", back_populates="paciente")

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(Integer)
    sexo = Column(String)
    fecha_nacimiento = Column(String)
    lugar_nacimiento = Column(String)
    domicilio = Column(String)
    n_casa = Column(String)
    zona_barrio = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    estado_civil = Column(String)
    profesion_oficio = Column(String)
    paciente = relationship("Paciente", back_populates="declaraciones")

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    p1 = Column(String); d1 = Column(String)
    p2 = Column(String); d2 = Column(String)
    p3 = Column(String); d3 = Column(String)
    p4 = Column(String); d4 = Column(String)
    p5 = Column(String); d5 = Column(String)
    p6 = Column(String); d6 = Column(String)
    p7 = Column(String); d7 = Column(String)
    p8 = Column(String); d8 = Column(String)
    p9 = Column(String); d9 = Column(String)
    p10 = Column(String); d10 = Column(String)
    p11 = Column(String); d11 = Column(String)
    p12 = Column(String); d12 = Column(String)
    cirugias = Column(String)
    accidentes = Column(String)
    paciente = relationship("Paciente", back_populates="antecedentes")

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_riesgos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fuma = Column(String)
    bebe = Column(String)
    drogas = Column(String)
    coca = Column(String)
    deportes = Column(String)
    grupo_sanguineo = Column(String)
    paciente = relationship("Paciente", back_populates="habitos_riesgos")
