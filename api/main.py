from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear tablas en PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# CONFIGURACIÓN DE CORS: Totalmente abierta para evitar bloqueos del navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Servidor Activo - Proyecto en la Nube"}

# --- RUTAS PARA PACIENTES (Acepta con y sin /) ---
@app.post("/pacientes", response_model=schemas.Paciente)
@app.post("/pacientes/", response_model=schemas.Paciente, include_in_schema=False)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- RUTAS PARA DECLARACIONES (Acepta con y sin /) ---
@app.post("/declaraciones/p1", response_model=schemas.DeclaracionJurada)
@app.post("/declaraciones/p1/", response_model=schemas.DeclaracionJurada, include_in_schema=False)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    return crud.create_declaracion_p1(db=db, declaracion=declaracion)

@app.get("/declaraciones/p1", response_model=List[schemas.DeclaracionJurada])
def read_declaraciones_p1(db: Session = Depends(get_db)):
    return db.query(models.DeclaracionJurada).all()
