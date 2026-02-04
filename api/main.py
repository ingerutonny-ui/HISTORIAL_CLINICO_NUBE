from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear tablas en PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# CONFIGURACIÓN DE CORS (CORREGIDO PARA EVITAR BLOQUEOS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (GitHub Pages, Local, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Configuración para ignorar barras diagonales al final
app.router.redirect_slashes = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Servidor Activo - CORS Liberado"}

# --- RUTAS PARA PACIENTES ---
@app.post("/pacientes", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- RUTAS PARA DECLARACIONES ---
@app.post("/declaraciones/p1", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    return crud.create_declaracion_p1(db=db, declaracion=declaracion)

@app.get("/declaraciones/p1", response_model=List[schemas.DeclaracionJurada])
def read_declaraciones_p1(db: Session = Depends(get_db)):
    return db.query(models.DeclaracionJurada).all()
