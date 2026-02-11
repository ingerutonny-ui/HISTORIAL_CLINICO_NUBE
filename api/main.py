from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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

@app.post("/pacientes/", response_model=schemas.PacienteCreate)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/")
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/filiacion/")
def create_filiacion(filiacion: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    return crud.create_filiacion(db=db, filiacion=filiacion)

@app.post("/antecedentes/")
def create_antecedentes(antecedentes: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=antecedentes)

@app.post("/habitos/")
def create_habitos(habitos: schemas.HabitosP3Create, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=habitos)
