from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
# Importación desde la carpeta api para el entorno de Vercel
from api import crud, models, schemas, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Eliminamos el prefijo /api/ de aquí porque vercel.json ya lo maneja
@app.get("/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

@app.post("/pacientes", response_model=schemas.Paciente)
def crear_nuevo_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.crear_paciente(db=db, paciente=paciente)

@app.get("/pacientes", response_model=List[schemas.Paciente])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_pacientes(db, skip=skip, limit=limit)
