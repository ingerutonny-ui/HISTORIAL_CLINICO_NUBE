import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Intentar usar la URL interna guardada en Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL")

# Si no existe, usar la URL por defecto como respaldo
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corregir el prefijo para compatibilidad con SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Crear el motor de base de datos
# Al ser conexión interna, no requiere parámetros de SSL manuales
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
