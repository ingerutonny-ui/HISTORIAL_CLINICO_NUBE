import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener la URL de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección de prefijo para SQLAlchemy 2.0+
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Se elimina cualquier argumento complejo y se deja que el driver maneje el SSL
# ya que tienes PGSSLMODE=require configurado en Render.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
