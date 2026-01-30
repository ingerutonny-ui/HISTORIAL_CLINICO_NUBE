from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal

# Inicialización de tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ÚNICA FORMA DE QUE LOS BOTONES FUNCIONEN:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que tu GitHub Pages se conecte
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
    return {"status": "Servidor HISTORIAL_CLINICO_NUBE activo"}

# Ruta para el botón CONSULTAR
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

# Ruta para el botón REGISTRAR
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="CI ya registrado")
    return crud.create_paciente(db=db, paciente=paciente)
