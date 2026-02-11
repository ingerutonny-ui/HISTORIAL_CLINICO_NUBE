import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Forzar la ruta al volumen persistente de Render
SQLALCHEMY_DATABASE_URL = "sqlite:////data/historial.db"

# Solo usa local si /data no existe (para que no falle al subir)
if not os.path.exists("/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./historial.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
