from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pacientes/", response_model=schemas.Paciente)
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/", response_model=list[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/filiacion/")
def guardar_p1(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/declaraciones/p2/")
def guardar_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/declaraciones/p3/")
def guardar_p3(data: schemas.HabitosP3Create, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=data)
