import os
import sys

# Esta línea es la clave: le dice a Python que busque archivos dentro de la carpeta actual
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

# Importamos directamente, ya que sys.path ahora incluye esta carpeta
import crud, models, schemas, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usamos la ruta raíz "/" porque vercel.json ya redirige /api/ aquí
@app.get("/")
@app.get("/api")
@app.get("/api/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

# ... (deja el resto de tus funciones post y get igual, pero asegúrate de que usen schemas.Paciente, etc.)
