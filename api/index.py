from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

# Importación relativa con punto para que funcione dentro de la carpeta api en Vercel
from . import crud, models, schemas, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz de la función
@app.get("/api")
@app.get("/api/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

@app.post("/api/pacientes", response_model=schemas.Paciente)
@app.post("/api/pacientes/", response_model=schemas.Paciente)
def crear_nuevo_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.crear_paciente(db=db, paciente=paciente)

@app.get("/api/pacientes", response_model=List[schemas.Paciente])
@app.get("/api/pacientes/", response_model=List[schemas.Paciente])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_pacientes(db, skip=skip, limit=limit)
