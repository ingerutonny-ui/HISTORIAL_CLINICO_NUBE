from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL obtenida del panel de entorno de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección de protocolo para compatibilidad con SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración del motor de base de datos con SSL obligatorio para Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

# --- BLOQUE DE LIMPIEZA DE TABLAS ---
# Este bloque borra las tablas para que se reconstruyan con los nombres 
# de columna correctos (documento_identidad y edad).
with engine.connect() as conn:
    try:
        conn.execute(text("DROP TABLE IF EXISTS declaraciones_juradas CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS pacientes CASCADE;"))
        conn.commit()
        print("Tablas antiguas eliminadas con éxito.")
    except Exception as e:
        print(f"Aviso en limpieza: {e}")
# ------------------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
