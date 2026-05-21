from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from . import models, database, crud

app = FastAPI(redirect_slashes=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo de datos para validación
class PersonalBase(BaseModel):
    ci: str
    nombre: str
    paterno: str
    turno: str
    especialidad: Optional[str] = None

@app.post("/doctor/")
def save_doctor(data: PersonalBase, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data.dict())

@app.post("/enfermera/")
def save_enfermera(data: PersonalBase, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data.dict())

@app.get("/doctores/")
def list_doctores(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

@app.get("/enfermeras/")
def list_enfermeras(db: Session = Depends(get_db)):
    return db.query(models.Enfermera).all()

# --- PACIENTES ---
@app.post("/pacientes/")
def save_paciente(data: dict, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data)

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
