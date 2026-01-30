from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crea las tablas automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CONFIGURACIÓN RADICAL DE CORS PARA ELIMINAR EL "FALLO DE RED"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier sitio (como tu GitHub)
    allow_credentials=False, # Cambiado a False para evitar conflictos de seguridad
    allow_methods=["GET", "POST", "OPTIONS"], # Métodos explícitos
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="Ya existe")
    return crud.create_paciente(db=db, paciente=paciente)
