import os
import time
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DEFINICIÓN DE LA RUTA AL DISCO PERSISTENTE (DISK de Render)
# Esta es la ruta que configuramos para que NO se borren los pacientes
SQLALCHEMY_DATABASE_URL = "sqlite:////data/historial.db"

# 2. VERIFICACIÓN DE ENTORNO
# Si no estamos en Render (carpeta /data no existe), usamos ruta local
if not os.path.exists("/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./historial.db"

# 3. CONFIGURACIÓN DEL MOTOR CON MANEJO DE BLOQUEOS (Timeout)
# "check_same_thread": False es necesario para que FastAPI maneje múltiples pedidos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False, "timeout": 30}
)

# 4. OPTIMIZACIÓN PARA SQLITE (Modo WAL)
# Esto evita que la base de datos se ponga "lenta" o se bloquee al escribir
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

# 5. CONFIGURACIÓN DE LA SESIÓN
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. BASE PARA LOS MODELOS
Base = declarative_base()
