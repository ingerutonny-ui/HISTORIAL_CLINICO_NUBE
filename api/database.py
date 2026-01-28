from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuración para SQLite (Windows 11 / Python)
# El archivo se creará en la raíz de tu proyecto
SQLALCHEMY_DATABASE_URL = "sqlite:///./historial_clinico.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definición del Modelo de Paciente
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    # Campo para el código único (ej: JD001)
    codigo_paciente = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    historia_clinica = Column(Text, nullable=True)

# 3. Creación automática de la tabla
Base.metadata.create_all(bind=engine)
