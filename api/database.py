import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Buscamos la URL de tu base de datos de $7 en el sistema de Render
# Si no la encuentra por algún motivo, usa SQLite como respaldo (solo para evitar que el servidor caiga)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./historial.db")

# Si la URL empieza con "postgres://", la corregimos a "postgresql://" para que SQLAlchemy la entienda
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuramos el motor de la base de datos
# Quitamos "check_same_thread" porque PostgreSQL maneja múltiples conexiones de forma segura
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
