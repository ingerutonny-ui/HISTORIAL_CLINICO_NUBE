from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Configuración de CORS corregida para permitir el acceso desde GitHub Pages
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

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.post("/filiacion/")
def save_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/declaraciones/p2/")
def save_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/declaraciones/p3/")
def save_p3(data: schemas.HabitosCreate, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=data)

@app.get("/historial/{paciente_id}")
def get_historial(paciente_id: int, db: Session = Depends(get_db)):
    historial = crud.get_historial_completo(db, paciente_id)
    if not historial["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return historial
