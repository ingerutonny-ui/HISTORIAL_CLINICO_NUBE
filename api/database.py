from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuración para SQLite en la nube (Vercel)
DATABASE_URL = "sqlite:///./historial_clinico.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Paciente
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    # Ejemplo: "JD001"
    codigo_paciente = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    historia_clinica = Column(Text, nullable=True)
    
    # Nuevo campo para reportes y auditoría
    fecha_registro = Column(DateTime, default=datetime.utcnow)

# Creación de tablas en el entorno de nube
Base.metadata.create_all(bind=engine)
