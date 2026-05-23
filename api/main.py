from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configurado para permitir todo desde cualquier origen
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

# RUTA DE SALUD (Para que Render no se cierre)
@app.get("/")
def read_root():
    return {"status": "ok"}

# RUTA EXPLÍCITA PARA PACIENTES
@app.get("/pacientes/")
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
