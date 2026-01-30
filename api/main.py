from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

# Importaciones de tu estructura de proyecto
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL CLINICO NUBE")

# 1. SOLUCIÓN AL ERROR DE CONEXIÓN: Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que tu GitHub Pages se conecte sin errores de red
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "Servidor en la Nube Activo"}

# 2. RUTA PARA CONSULTAR (Botón: Consultar Base de Datos)
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

# 3. RUTA PARA REGISTRAR (Botón: Registrar Paciente)
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="El CI ya existe en el sistema")
    return crud.create_paciente(db=db, paciente=paciente)
