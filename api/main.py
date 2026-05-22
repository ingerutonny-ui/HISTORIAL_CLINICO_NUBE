from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models, schemas

# Crear tablas
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

# --- PACIENTES ---
@app.post("/pacientes/")
def registrar_paciente(data: schemas.PacienteBase, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data.model_dump())

# --- DECLARACIÓN JURADA (P1) ---
@app.post("/filiacion/")
def registrar_filiacion(data: schemas.DeclaracionJuradaBase, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data.model_dump())

# --- ANTECEDENTES (P2) ---
@app.post("/antecedentes_p2/")
def registrar_p2(data: schemas.AntecedentesP2Base, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data.model_dump())

# --- HÁBITOS Y RIESGOS (P3) ---
@app.post("/habitos_p3/")
def registrar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data.model_dump())

# --- DOCTORES Y ENFERMERAS (INTEGRIDAD MANTENIDA) ---
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {
        "doctores": db.query(models.Doctor).all(), 
        "enfermeras": db.query(models.Enfermera).all()
    }

@app.post("/doctores/")
def registrar_doctor(data: schemas.DoctorBase, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data.model_dump())

@app.post("/enfermeras/")
def registrar_enfermera(data: schemas.EnfermeraBase, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data.model_dump())

@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="Doctor no encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor eliminado"}

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    db.delete(enfermera)
    db.commit()
    return {"message": "Enfermera eliminada"}
