from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

# Iniciamos la aplicación
app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

@app.post("/pacientes/", response_model=schemas.Paciente)
def crear_nuevo_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.crear_paciente(db=db, paciente=paciente)

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_pacientes(db, skip=skip, limit=limit)
