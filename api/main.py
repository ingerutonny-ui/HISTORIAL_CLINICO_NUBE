from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crea las tablas automáticamente al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ESTA ES LA CLAVE: Permite comunicación total con GitHub
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
def root():
    return {"status": "Servidor en la Nube Activo"}

# Ruta para CONSULTAR
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

# Ruta para REGISTRAR (Aquí estaba el conflicto de nombres)
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    # Verificamos si el documento ya existe
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="Documento ya registrado")
    return crud.create_paciente(db=db, paciente=paciente)
