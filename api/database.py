import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener URL de Render
raw_url = os.getenv("DATABASE_URL")

def fix_render_url(url: str):
    if not url:
        return url
    # SQLAlchemy requiere postgresql:// en lugar de postgres://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    # Eliminar cualquier parámetro previo de sslmode para evitar duplicados
    if "?sslmode=" in url:
        url = url.split("?sslmode=")[0]
    return url

SQLALCHEMY_DATABASE_URL = fix_render_url(raw_url)

# Conexión forzada con SSL requerida por Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
