from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Esta línea busca la URL que configuraste en el panel de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Si por alguna razón no la encuentra, usamos la de Virginia de tu captura directamente
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://render_user_wtbi_user:9jfdjWfJOQQ5gv6kw6sabwMjIlMUAF51@dpg-d5tobtp4tr6s738okvdg-a.virginia-postgres.render.com/render_user_wtbi"

# Corrección de protocolo para SQLAlchemy (de postgres:// a postgresql://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Motor de conexión con seguridad SSL obligatoria
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
