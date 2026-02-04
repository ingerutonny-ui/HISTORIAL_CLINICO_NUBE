from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    documento_identidad = Column(String, unique=True, index=True)
    codigo_paciente = Column(String, unique=True)
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))

    # SECCIÓN 1: AFILIACIÓN
    edad = Column(Integer, nullable=True)
    sexo = Column(String, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)
    fecha_nacimiento = Column(String, nullable=True)
    estado_civil = Column(String, nullable=True)
    domicilio = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    profesion_oficio = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="declaraciones")
