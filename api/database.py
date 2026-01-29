from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Render inyecta esto directamente desde el panel que configuramos
DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección de protocolo para SQLAlchemy 1.4+
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# El motor con SSL es obligatorio en Render
engine = create_engine(
    DATABASE_URL, 
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
