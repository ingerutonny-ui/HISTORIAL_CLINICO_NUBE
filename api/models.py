from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "filiacion_p1"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(Integer)
    sexo = Column(String)
    fecha_nacimiento = Column(Date)
    estado_civil = Column(String)
    lugar_nacimiento = Column(String)
    domicilio = Column(String)
    n_casa = Column(String)
    zona_barrio = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    profesion_oficio = Column(String)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    p1 = Column(String); d1 = Column(String); p2 = Column(String); d2 = Column(String)
    p3 = Column(String); d3 = Column(String); p4 = Column(String); d4 = Column(String)
    p5 = Column(String); d5 = Column(String); p6 = Column(String); d6 = Column(String)
    p7 = Column(String); d7 = Column(String); p8 = Column(String); d8 = Column(String)
    p9 = Column(String); d9 = Column(String); p10 = Column(String); d10 = Column(String)
    p11 = Column(String); d11 = Column(String); p12 = Column(String); d12 = Column(String)
    p13 = Column(String); d13 = Column(String); p14 = Column(String); d14 = Column(String)
    p15 = Column(String); d15 = Column(String); p16 = Column(String); d16 = Column(String)
    p17 = Column(String); d17 = Column(String); p18 = Column(String); d18 = Column(String)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    deportes_si_no = Column(String)
    deportes_detalle = Column(String)
    accidentes_si_no = Column(String)
    accidentes_detalle = Column(String)
    medicamentos_si_no = Column(String)
    medicamentos_detalle = Column(String)
    grupo_sanguineo = Column(String)
    historia_laboral = Column(String)
    riesgos_vida_laboral = Column(String) # Campo recuperado
