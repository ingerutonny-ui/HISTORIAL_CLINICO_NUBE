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

    # Campos para las 11 preguntas (p) y sus detalles (d)
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

    paciente = relationship("Paciente", back_populates="antecedentes")
