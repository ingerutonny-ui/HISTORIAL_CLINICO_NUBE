from sqlalchemy import Column, Integer, String
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    ci = Column(String, unique=True, index=True)
    fecha_ingreso = Column(String)
    codigo = Column(String, unique=True)
