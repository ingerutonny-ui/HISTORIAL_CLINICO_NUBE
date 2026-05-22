from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
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

# --- Rutas Doctores ---
@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data)

@app.put("/doctores/{id_doc}")
def editar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    for key, value in data.items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

# --- Rutas Enfermeras ---
@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data)

@app.put("/enfermeras/{id_enfe}")
def editar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    for key, value in data.items():
        setattr(enfermera, key, value)
    db.commit()
    db.refresh(enfermera)
    return enfermera

# --- Rutas Pacientes ---
@app.post("/paciente/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data)

@app.post("/antecedentes_p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data)

@app.post("/habitos_p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data)

@app.delete("/paciente/{paciente_id}")
def borrar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado"}

@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    doctores = db.query(models.Doctor).all()
    enfermeras = db.query(models.Enfermera).all()
    return {"doctores": doctores, "enfermeras": enfermeras}
