from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# Configuración de CORS para permitir conexión desde el Frontend
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
    return {"status": "Servidor HISTORIAL_CLINICO_NUBE activo y profesional"}

#--- RUTAS DE PACIENTES ---

@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_ci(db, ci=paciente.documento_identidad)
    if db_paciente:
        raise HTTPException(status_code=400, detail="Documento de identidad ya registrado")
    return crud.create_paciente(db=db, paciente=paciente)

#--- RUTAS DE DECLARACIÓN JURADA ---

@app.get("/declaraciones", response_model=List[schemas.DeclaracionJurada])
def read_declaraciones(db: Session = Depends(get_db)):
    return crud.get_declaraciones(db)

@app.post("/declaraciones/", response_model=schemas.DeclaracionJurada)
def create_declaracion(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    # El método crud ya maneja todos los nuevos campos automáticamente
    return crud.create_declaracion_jurada(db=db, declaracion=declaracion)
