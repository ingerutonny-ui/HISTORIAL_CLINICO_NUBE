from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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

@app.get("/")
async def root():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS DE PACIENTES (P1, P2, P3) ---

@app.post("/api/save-p1")
async def save_p1(data: schemas.DeclaracionJuradaBase, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data.model_dump())

@app.post("/api/save-p2")
async def save_p2(data: schemas.AntecedentesP2Base, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data.model_dump())

@app.post("/api/save-p3")
async def save_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data.model_dump())

# --- RUTAS DE PERSONAL MÉDICO (DOCTORES Y ENFERMERAS) ---

@app.post("/api/save-doctor")
async def save_doctor(data: schemas.DoctorBase, db: Session = Depends(get_db)):
    """Ruta para registrar o actualizar médicos en la nube"""
    return crud.upsert_doctor(db, data.model_dump())

@app.post("/api/save-enfermera")
async def save_enfermera(data: schemas.EnfermeraBase, db: Session = Depends(get_db)):
    """Ruta para registrar o actualizar enfermeras en la nube"""
    return crud.upsert_enfermera(db, data.model_dump())
