from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models

# Inicializa la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración CORS esencial
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos las rutas de forma simple y directa
@app.get("/")
def read_root():
    return {"status": "ok"}

# Esta es la ruta que tu frontend intenta consultar
@app.get("/pacientes/")
def get_pacientes():
    from .database import SessionLocal
    from .models import Paciente
    db = SessionLocal()
    try:
        pacientes = db.query(Paciente).all()
        return pacientes
    finally:
        db.close()
