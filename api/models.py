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
    # Cubrimos los 18 sistemas del formulario oficial
    p1 = Column(String); d1 = Column(String) # Vista
    p2 = Column(String); d2 = Column(String) # Auditivo
    p3 = Column(String); d3 = Column(String) # Respiratorios
    p4 = Column(String); d4 = Column(String) # Cardio-vasculares
    p5 = Column(String); d5 = Column(String) # Estomago/Intestino
    p6 = Column(String); d6 = Column(String) # Genito/Urinario
    p7 = Column(String); d7 = Column(String) # Sistema Nervioso
    p8 = Column(String); d8 = Column(String) # Psiquiatricos
    p9 = Column(String); d9 = Column(String) # Osteomusculares
    p10 = Column(String); d10 = Column(String) # Piel/Dermatologicas
    p11 = Column(String); d11 = Column(String) # Alergias
    p12 = Column(String); d12 = Column(String) # Cirugias
    p13 = Column(String); d13 = Column(String) # Accidentes Trabajo
    p14 = Column(String); d14 = Column(String) # Accidentes Particulares
    p15 = Column(String); d15 = Column(String) # Medicamentos
    p16 = Column(String); d16 = Column(String) # Infecciosas
    p17 = Column(String); d17 = Column(String) # Otros
    p18 = Column(String); d18 = Column(String) # Ginecologia (si aplica)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    h1 = Column(String); r1 = Column(String) # Tabaco
    h2 = Column(String); r2 = Column(String) # Alcohol
    h3 = Column(String); r3 = Column(String) # Drogas
    h4 = Column(String); r4 = Column(String) # Coca/Pijchar
    h5 = Column(String); r5 = Column(String) # Deportes
    h6 = Column(String); r6 = Column(String) # Riesgos Fisicos
    h7 = Column(String); r7 = Column(String) # Riesgos Quimicos
    h8 = Column(String); r8 = Column(String) # Riesgos Ergonomicos
    h9 = Column(String); r9 = Column(String) # Riesgos Psicologicos
    h10 = Column(String); r10 = Column(String) # Grupo Sanguineo
    # Campo para la tabla de Historia Laboral (Hoja 2)
    historia_laboral = Column(Text, default="[]")
