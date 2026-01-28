from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import os
import sys

# Asegura que Python encuentre los archivos locales en Vercel
sys.path.append(os.path.dirname(__file__))

import crud, schemas, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
@app.get("/api/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

@app.get("/api/pacientes", response_model=List[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return crud.obtener_pacientes(db)
