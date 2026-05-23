from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
import logging

# Configurar logs para ver qué está pasando
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

# RUTA DEFINIDA DE FORMA PLANA Y SIN DEPENDENCIAS DE SESSION DURANTE EL ARRANQUE
@app.get("/pacientes/")
def get_pacientes():
    logger.info("Recibida petición en /pacientes/")
    from .database import SessionLocal
    from .models import Paciente
    db = SessionLocal()
    try:
        pacientes = db.query(Paciente).all()
        return pacientes
    except Exception as e:
        logger.error(f"Error al obtener pacientes: {e}")
        return []
    finally:
        db.close()
