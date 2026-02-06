from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True, index=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "filiacion"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(Integer)
    sexo = Column(String)
    fecha_nacimiento = Column(Date)
    lugar_nacimiento = Column(String)
    domicilio = Column(String)
    n_casa = Column(String)
    zona_barrio = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    estado_civil = Column(String)
    profesion_oficio = Column(String)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    p1 = Column(String); d1 = Column(String); p2 = Column(String); d2 = Column(String); p3 = Column(String); d3 = Column(String)
    p4 = Column(String); d4 = Column(String); p5 = Column(String); d5 = Column(String); p6 = Column(String); d6 = Column(String)
    p7 = Column(String); d7 = Column(String); p8 = Column(String); d8 = Column(String); p9 = Column(String); d9 = Column(String)
    p10 = Column(String); d10 = Column(String); p11 = Column(String); d11 = Column(String); p12 = Column(String); d12 = Column(String)
    p13 = Column(String); d13 = Column(String); p14 = Column(String); d14 = Column(String); p15 = Column(String); d15 = Column(String)
    p16 = Column(String); d16 = Column(String); p17 = Column(String); d17 = Column(String); p18 = Column(String); d18 = Column(String)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    h1 = Column(String); r1 = Column(String); h2 = Column(String); r2 = Column(String); h3 = Column(String); r3 = Column(String)
    h4 = Column(String); r4 = Column(String); h5 = Column(String); r5 = Column(String); h6 = Column(String); r6 = Column(String)
    h7 = Column(String); r7 = Column(String); h8 = Column(String); r8 = Column(String); h9 = Column(String); r9 = Column(String)
    h10 = Column(String); r10 = Column(String)
    historia_laboral = Column(Text)
