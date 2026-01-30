from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Importaciones relativas para estructura de nube
from . import models, schemas, crud
from .database import engine, SessionLocal

# Crea las tablas automáticamente con la estructura de pacientes y declaraciones
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# LA SOLUCIÓN AL FALLO DE RED: Configuración total de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que tu GitHub Pages se conecte
    allow_credentials=True,
    allow_methods=["*"],  # Permite POST, GET, etc.
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
def home():
    return {"status": "Servidor en la Nube Activo"}

# Ruta para CONSULTAR (Botón inferior)
@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pacientes(db, skip=skip, limit=limit)

# Ruta para REGISTRAR (Botón principal)
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="El Documento de Identidad ya existe")
    return crud.create_paciente(db=db, paciente=paciente)
