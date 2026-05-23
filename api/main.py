from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import create_paciente, delete_paciente, upsert_filiacion, upsert_p2, upsert_p3, create_doctor, create_enfermera
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- PACIENTES ---

@app.get("/api/paciente-completo/{codigo_ingresado}")
def obtener_paciente_completo(codigo_ingresado: str, db: Session = Depends(get_db)):
    # Búsqueda estricta por codigo_paciente
    paciente = db.query(models.Paciente).filter(
        models.Paciente.codigo_paciente == codigo_ingresado
    ).first()
    
    if not paciente: 
        raise HTTPException(status_code=404, detail="CÓDIGO NO ENCONTRADO")
        
    return {
        "paciente": paciente,
        "filiacion": db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente.id).first(),
        "antecedentes": db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente.id).first(),
        "habitos": db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente.id).first()
    }

@app.post("/pacientes/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)): return create_paciente(db, data)

@app.get("/pacientes/")
def listar_todos_los_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.delete("/api/pacientes/{paciente_id}")
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    exito = delete_paciente(db, paciente_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado correctamente"}

# --- FILIACIÓN Y ANTECEDENTES ---

@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)): return upsert_filiacion(db, data)

@app.post("/p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)): return upsert_p2(db, data)

@app.post("/p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)): return upsert_p3(db, data)

# --- PERSONAL ---

@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {"doctores": db.query(models.Doctor).all(), "enfermeras": db.query(models.Enfermera).all()}

@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)): return create_doctor(db, data)

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.items(): setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Eliminado"}

@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)): return create_enfermera(db, data)

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    for key, value in data.items(): setattr(enfermera, key, value)
    db.commit()
    db.refresh(enfermera)
    return enfermera

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    db.delete(enfermera)
    db.commit()
    return {"message": "Eliminada"}
