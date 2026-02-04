from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear tablas en PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"status": "Servidor Limpio - Listo para Parte 1"}

# RUTA PARA GUARDAR (POST)
@app.post("/declaraciones/p1", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    return crud.create_declaracion_p1(db=db, declaracion=declaracion)

# RUTA PARA VERIFICAR DATOS (GET) - AÑADIDA PARA VALIDACIÓN
@app.get("/declaraciones/p1", response_model=List[schemas.DeclaracionJurada])
def read_declaraciones_p1(db: Session = Depends(get_db)):
    return db.query(models.DeclaracionJurada).all()
