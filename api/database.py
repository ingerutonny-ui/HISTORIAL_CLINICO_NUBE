import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Prioridad total a la variable que creamos manualmente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL")

# 2. Respaldo por seguridad
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Forzar el protocolo correcto para Render/PostgreSQL
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Motor con configuración de reconexión automática (evita el 500 por desconexión)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. COMANDO CRÍTICO: Forzar la creación de tablas cada vez que el código inicie
from . import models
try:
    models.Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas correctamente.")
except Exception as e:
    print(f"Error creando tablas: {e}")
