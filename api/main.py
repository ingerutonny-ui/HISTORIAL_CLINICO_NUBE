from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "API HISTORIAL_CLINICO_NUBE funcionando"}

@app.post("/filiacion/")
def guardar_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    # Esta ruta procesa el formulario de la captura image_3b09fe.png
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/pacientes/")
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/declaraciones/p2/")
def guardar_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/declaraciones/p3/")
def guardar_p3(data: schemas.HabitosP3Create, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=data)
