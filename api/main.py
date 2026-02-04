from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Intentar crear/actualizar tablas al iniciar
try:
    models.Base.metadata.create_all(bind=engine)
    print("Base de datos conectada y tablas verificadas.")
except Exception as e:
    print(f"Error crítico de conexión: {e}")

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# CORS abierto para que GitHub Pages no sea bloqueado
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
    return {"status": "ONLINE", "database": "CONNECTED"}

@app.post("/pacientes", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_paciente(db=db, paciente=paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/declaraciones/p1", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_declaracion_p1(db=db, declaracion=declaracion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/declaraciones/p1", response_model=List[schemas.DeclaracionJurada])
def read_declaraciones_p1(db: Session = Depends(get_db)):
    return db.query(models.DeclaracionJurada).all()
