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
    # Relación con la nueva tabla de antecedentes
    antecedentes = relationship("AntecedentesP2", back_populates="paciente")
    # Relación con la tercera sección
    habitos_riesgos = relationship("HabitosRiesgosP3", back_populates="paciente")

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    
    edad = Column(String) 
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

# ============================================================
# INICIO DE LA SEGUNDA SECCIÓN - ANTECEDENTES PATOLÓGICOS
# ============================================================

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))

    # Campos para los 22 datos (11 indicadores 'p' y 11 detalles 'd')
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
    p13 = Column(String); d13 = Column(String)
    p14 = Column(String); d14 = Column(String)
    p15 = Column(String); d15 = Column(String)
    p16 = Column(String); d16 = Column(String)
    p17 = Column(String); d17 = Column(String)
    p18 = Column(String); d18 = Column(String)
    p19 = Column(String); d19 = Column(String)
    p20 = Column(String); d20 = Column(String)
    p21 = Column(String); d21 = Column(String)
    p22 = Column(String); d22 = Column(String)

    paciente = relationship("Paciente", back_populates="antecedentes")

# ============================================================
# INICIO DE LA TERCERA SECCIÓN - HÁBITOS Y RIESGOS
# ============================================================

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_riesgos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))

    # Hábitos Personales
    fuma = Column(String)
    fuma_det = Column(String)
    bebe = Column(String)
    bebe_det = Column(String)
    drogas = Column(String)
    drogas_det = Column(String)
    meds = Column(String)
    meds_det = Column(String)

    # Antecedentes Ocupacionales
    historial_lab = Column(String)

    # Antecedentes de Riesgo
    r_fisico = Column(String)
    r_ergonomico = Column(String)
    r_quimico = Column(String)
    r_psico = Column(String)
    r_obs = Column(String)

    paciente = relationship("Paciente", back_populates="habitos_riesgos")
