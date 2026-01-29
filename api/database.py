from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Render ya tiene la DATABASE_URL en su panel, la tomamos directamente
DATABASE_URL = os.getenv("DATABASE_URL")

# Si la URL empieza con 'postgres://', la cambiamos a 'postgresql://' (exigencia de SQLAlchemy)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Creamos el motor con el modo SSL requerido para Render
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
