from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    ci = Column(String, unique=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_p1"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
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

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    datos_json = Column(Text)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    # Almacenamos los 22 campos del JSON de P3 aquí
    datos_p3 = Column(Text)
