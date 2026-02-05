from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

try:
    models.Base.metadata.create_all(bind=engine)
    print("Base de datos conectada y tablas verificadas.")
except Exception as e:
    print(f"Error crítico de conexión: {e}")

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

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

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_paciente(db=db, paciente=paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p1/", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_declaracion_p1(db=db, declaracion=declaracion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p2/", response_model=schemas.AntecedentesP2)
def save_p2(antecedentes: schemas.AntecedentesP2Create, db: Session = Depends(get_db)):
    try:
        return crud.create_antecedentes_p2(db=db, antecedentes=antecedentes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p3/", response_model=schemas.HabitosRiesgosP3)
def save_p3(habitos: schemas.HabitosRiesgosP3Create, db: Session = Depends(get_db)):
    try:
        return crud.create_habitos_p3(db=db, habitos=habitos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
