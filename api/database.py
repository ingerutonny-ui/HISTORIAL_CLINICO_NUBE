import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usamos la URL de PostgreSQL que Render te proporciona en Variables de Entorno
# Si no existe, usamos una por defecto para evitar que el sistema falle al arrancar
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")

# Ajuste para compatibilidad con SQLAlchemy 2.0 y Render
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
