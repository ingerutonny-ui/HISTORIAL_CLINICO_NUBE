import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener URL de Render
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración optimizada para Render y PostgreSQL
engine = create_engine(
    DATABASE_URL, 
    pool_size=10,             # Mantiene hasta 10 conexiones abiertas
    max_overflow=20,          # Permite hasta 20 conexiones extra en picos de carga
    pool_timeout=30,          # Tiempo de espera antes de dar error de conexión
    pool_recycle=1800,        # Reinicia conexiones cada 30 min para evitar bloqueos
    pool_pre_ping=True,       # Verifica si la conexión está viva antes de usarla
    connect_args={'connect_timeout': 10}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
