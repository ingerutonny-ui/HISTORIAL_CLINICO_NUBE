from sqlalchemy import Column, Integer, str, Date, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(str)
    apellidos = Column(str)
    ci = Column(str, unique=True, index=True)
    codigo_paciente = Column(str)

class DeclaracionJurada(Base):
    __tablename__ = "filiacion"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(Integer)
    sexo = Column(str)
    fecha_nacimiento = Column(Date)
    lugar_nacimiento = Column(str)
    domicilio = Column(str)
    n_casa = Column(str)
    zona_barrio = Column(str)
    ciudad = Column(str)
    pais = Column(str)
    telefono = Column(str)
    estado_civil = Column(str)
    profesion_oficio = Column(str)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    p1 = Column(str); d1 = Column(str); p2 = Column(str); d2 = Column(str); p3 = Column(str); d3 = Column(str)
    p4 = Column(str); d4 = Column(str); p5 = Column(str); d5 = Column(str); p6 = Column(str); d6 = Column(str)
    p7 = Column(str); d7 = Column(str); p8 = Column(str); d8 = Column(str); p9 = Column(str); d9 = Column(str)
    p10 = Column(str); d10 = Column(str); p11 = Column(str); d11 = Column(str); p12 = Column(str); d12 = Column(str)
    p13 = Column(str); d13 = Column(str); p14 = Column(str); d14 = Column(str); p15 = Column(str); d15 = Column(str)
    p16 = Column(str); d16 = Column(str); p17 = Column(str); d17 = Column(str); p18 = Column(str); d18 = Column(str)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    h1 = Column(str); r1 = Column(str); h2 = Column(str); r2 = Column(str); h3 = Column(str); r3 = Column(str)
    h4 = Column(str); r4 = Column(str); h5 = Column(str); r5 = Column(str); h6 = Column(str); r6 = Column(str)
    h7 = Column(str); r7 = Column(str); h8 = Column(str); r8 = Column(str); h9 = Column(str); r9 = Column(str)
    h10 = Column(str); r10 = Column(str)
    historia_laboral = Column(Text) # Aquí se guarda el JSON de la tabla
