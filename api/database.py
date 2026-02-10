import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL interna para comunicación privada en Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL")

# Si no existe la interna, usar la general (emergencia)
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección de protocolo para SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Motor sin SSL forzado (la red interna de Render es segura por defecto)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
