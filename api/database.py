from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL desde el panel de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección de protocolo para SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Motor estable y seguro
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

# --- LIMPIEZA DE TABLAS PARA CORREGIR COLUMNAS FALTANTES ---
# Esto borrará las tablas viejas para que se creen con 'cedula' y 'edad'
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS declaraciones_juradas CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS pacientes CASCADE;"))
    conn.commit()
# ---------------------------------------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
