from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Usaremos SQLite dentro del disco persistente /data que configuramos en Render
# Esto garantiza que los datos NO se borren al reiniciar
DATABASE_PATH = "/data/historial_clinico.db"

# Si estamos en local (fuera de Render), usamos una ruta temporal
if not os.path.exists("/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./historial_clinico_nube.db"
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Motor de conexión para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Se elimina el bloque de limpieza (DROP TABLE) para que los datos sean PERMANENTES
# Ya no se resetearán las tablas al iniciar el servidor

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
