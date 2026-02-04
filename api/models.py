from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True, index=True) # Cambio realizado aquí
    codigo_paciente = Column(String, unique=True)
    
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")

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
