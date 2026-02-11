import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ruta absoluta al DISK persistente
SQLALCHEMY_DATABASE_URL = "sqlite:////data/historial.db"

if not os.path.exists("/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./historial.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
