from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Importaciones relativas seguras para Render
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crea todas las tablas (Pacientes y Declaraciones) al iniciar el servidor
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# CONFIGURACIÓN DE SEGURIDAD (CORS): Vital para que funcionen los botones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para conectar a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensaje": "Servidor HISTORIAL_CLINICO_NUBE Activo y Sincronizado"}

# Ruta para el botón CONSULTAR BASE DE DATOS
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes

# Ruta para el botón REGISTRAR PACIENTE
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="El Documento de Identidad ya existe")
    return crud.create_paciente(db=db, paciente=paciente)
