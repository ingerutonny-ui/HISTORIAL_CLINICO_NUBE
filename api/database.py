from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# En Vercel, el único lugar con permiso de escritura es /tmp/
SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/pacientes.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    dni = Column(String, unique=True, index=True)
    fecha_ingreso = Column(String)
    codigo = Column(String, unique=True)

# Crear la tabla si no existe
Base.metadata.create_all(bind=engine)
