import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# FORZAR el uso de la URL interna de Render (la que termina en .internal)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL")

# Si la variable no se cargó correctamente, usamos la de respaldo
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Estandarizar el protocolo para SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Crear motor sin SSL manual (la red privada de Render no lo requiere)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
