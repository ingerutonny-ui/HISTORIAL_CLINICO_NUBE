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
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(String)
    sexo = Column(String)
    fecha_nacimiento = Column(String)
    lugar_nacimiento = Column(String)
    domicilio = Column(String)
    n_casa = Column(String, default="")
    zona_barrio = Column(String, default="") # Actualizado
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String, default="")
    estado_civil = Column(String)
    profesion_oficio = Column(String, default="") # Actualizado

class AntecedentesP2(Base):
    __tablename__ = "declaraciones_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    vista = Column(String, default="NO")
    # ... (el resto se mantiene igual para no arruinar la estructura)
    generales = Column(String, default="NO")
    generales_obs = Column(Text, default="")

class HabitosRiesgosP3(Base):
    __tablename__ = "declaraciones_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fuma = Column(String, default="NO")
    bebe_alcohol = Column(String, default="NO")
    deporte = Column(String, default="NO")
    observaciones = Column(Text, default="")
