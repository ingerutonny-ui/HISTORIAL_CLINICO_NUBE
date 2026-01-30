from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crea las tablas en la base de datos al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL CLINICO NUBE")

# CONFIGURACIÓN CERTERA DE CORS
# Esto permite que tu página de GitHub se comunique con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Abre la puerta a cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, etc.
    allow_headers=["*"],
)

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Servidor en la Nube Activo"}

# Endpoint para CONSULTAR (GET)
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

# Endpoint para REGISTRAR (POST)
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="El CI ya existe")
    return crud.create_paciente(db=db, paciente=paciente)
