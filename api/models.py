from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True, index=True)
    codigo_paciente = Column(String, unique=True)

class DeclaracionJurada(Base):
    __tablename__ = "filiaciones"
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
    # Los 18 campos del PDF Hoja 1
    p1 = Column(String); d1 = Column(String) # Vista
    p2 = Column(String); d2 = Column(String) # Auditivo
    p3 = Column(String); d3 = Column(String) # Respiratorios
    p4 = Column(String); d4 = Column(String) # Cardio
    p5 = Column(String); d5 = Column(String) # Digestivos
    p6 = Column(String); d6 = Column(String) # Sangre
    p7 = Column(String); d7 = Column(String) # Genitourinario
    p8 = Column(String); d8 = Column(String) # Nervioso
    p9 = Column(String); d9 = Column(String) # Psiquiatrico
    p10 = Column(String); d10 = Column(String) # Osteomuscular
    p11 = Column(String); d11 = Column(String) # Piel
    p12 = Column(String); d12 = Column(String) # Alergias
    p13 = Column(String); d13 = Column(String) # Cirugias
    p14 = Column(String); d14 = Column(String) # Accid. Trabajo
    p15 = Column(String); d15 = Column(String) # Accid. Particulares
    p16 = Column(String); d16 = Column(String) # Medicamentos
    p17 = Column(String); d17 = Column(String) # Infecciosas
    p18 = Column(String); d18 = Column(String) # Otros

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    h1 = Column(String); r1 = Column(String) # Tabaco
    h2 = Column(String); r2 = Column(String) # Alcohol
    h3 = Column(String); r3 = Column(String) # Drogas
    h4 = Column(String); r4 = Column(String) # Pijchar
    h5 = Column(String); r5 = Column(String) # Deportes
    h6 = Column(String); r6 = Column(String) # Riesgos Fisicos
    h7 = Column(String); r7 = Column(String) # Riesgos Quimicos
    h8 = Column(String); r8 = Column(String) # Riesgos Ergonomicos
    h9 = Column(String); r9 = Column(String) # Riesgos Psicologicos
    h10 = Column(String); r10 = Column(String) # Grupo Sanguineo
    historia_laboral = Column(Text, default="[]") # La tabla de la Hoja 2
