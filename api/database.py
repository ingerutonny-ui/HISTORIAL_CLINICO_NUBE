import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# BLINDAJE: El sistema buscará la URL de PostgreSQL configurada en Render
# Esto evita que el colaborador vea tus credenciales reales.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección necesaria para compatibilidad de SQLAlchemy con Render
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuramos el motor para PostgreSQL (sin los argumentos de SQLite)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
