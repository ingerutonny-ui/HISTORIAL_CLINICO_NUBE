import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión de Render
raw_url = os.getenv("DATABASE_URL")

def get_final_url(url: str):
    if not url:
        return url
    # Corregir prefijo para SQLAlchemy
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    # Limpiar parámetros previos
    if "?" in url:
        url = url.split("?")[0]
    return url

SQLALCHEMY_DATABASE_URL = get_final_url(raw_url)

# Configuración de motor específica para PostgreSQL en Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    },
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
