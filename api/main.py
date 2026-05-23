from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS abierto
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

@app.get("/pacientes/")
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.get("/")
def read_root():
    return {"status": "ok"}
