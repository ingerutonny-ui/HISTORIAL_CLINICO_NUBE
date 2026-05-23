from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuración básica de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esta ruta SÍ o SÍ mantendrá el servidor vivo para Render
@app.get("/")
def health_check():
    return {"status": "ok"}

# La conexión a DB ocurre SOLO cuando alguien pide pacientes
@app.get("/pacientes/")
def get_pacientes():
    logger.info("Intentando conectar a DB para /pacientes/")
    try:
        from .database import SessionLocal
        from .models import Paciente
        db = SessionLocal()
        pacientes = db.query(Paciente).all()
        db.close()
        return pacientes
    except Exception as e:
        logger.error(f"Error crítico en DB: {e}")
        return {"error": "DB_CONNECTION_FAILED"}
