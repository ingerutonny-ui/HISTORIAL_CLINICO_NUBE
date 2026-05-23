from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración CORS
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

# RUTA DE SALUD
@app.get("/")
def health_check():
    return {"status": "ok"}

# RUTA LISTA PACIENTES
@app.get("/pacientes/")
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
