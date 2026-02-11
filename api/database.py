import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definición de la ruta al DISK persistente de Render
SQLALCHEMY_DATABASE_URL = "sqlite:////data/historial.db"

# Si no estamos en Render, usamos ruta local para pruebas
if not os.path.exists("/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./historial.db"

# 2. Motor con manejo de bloqueos para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False, "timeout": 30}
)

# 3. Optimización para evitar que SQLite se bloquee
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
