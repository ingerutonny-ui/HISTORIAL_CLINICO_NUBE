from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

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
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data)

# --- DECLARACIÓN JURADA (P1) ---
@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data)

# --- ANTECEDENTES (P2) ---
@app.post("/antecedentes_p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data)

# --- HÁBITOS Y RIESGOS (P3) ---
@app.post("/habitos_p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data)

# --- PERSONAL ---
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {
        "doctores": db.query(models.Doctor).all(), 
        "enfermeras": db.query(models.Enfermera).all()
    }

# --- DOCTORES (POST para crear, PUT para editar) ---
@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data)

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

# --- ENFERMERAS (POST para crear, PUT para editar) ---
@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data)

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera:
        raise HTTPException(status_code=404, detail="No encontrada")
    for key, value in data.items():
        setattr(enfermera, key, value)
    db.commit()
    db.refresh(enfermera)
    return enfermera

# --- ELIMINACIÓN ---
@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Eliminado"}

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    db.delete(enfermera)
    db.commit()
    return {"message": "Eliminada"}
