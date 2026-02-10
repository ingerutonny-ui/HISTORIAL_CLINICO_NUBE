import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos la ruta al archivo en tu DISK de Render
# Ajusta 'database_disk' si el nombre de tu Mount Path es distinto
DB_PATH = "/opt/render/project/src/data/historial.db"

# Asegurar que el directorio exista para evitar errores de escritura
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 2. Motor específico para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Requerido para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Crear las tablas automáticamente al conectar
from . import models
models.Base.metadata.create_all(bind=engine)
