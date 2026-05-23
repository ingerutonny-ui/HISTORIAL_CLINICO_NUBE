from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración CORS para permitir la conexión desde tu frontend
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

# --- RUTAS DE PACIENTES ---
@app.get("/pacientes/")
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)): 
    return crud.create_paciente(db, data)

@app.delete("/pacientes/{id}")
def eliminar_paciente(id: int, db: Session = Depends(get_db)):
    if crud.delete_paciente(db, id):
        return {"message": "Eliminado con éxito"}
    raise HTTPException(status_code=404, detail="Paciente no encontrado")

# --- RUTAS DE SECCIONES ---
@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)): 
    return crud.upsert_filiacion(db, data)

@app.post("/p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)): 
    return crud.upsert_p2(db, data)

@app.post("/p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)): 
    return crud.upsert_p3(db, data)

@app.get("/api/paciente-completo/{identificador}")
def obtener_paciente_completo(identificador: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(
        (models.Paciente.codigo_paciente == identificador) | 
        (models.Paciente.id == (int(identificador) if identificador.isdigit() else 0))
    ).first()
    if not paciente: 
        raise HTTPException(status_code=404, detail="No encontrado")
    return {
        "paciente": paciente,
        "filiacion": db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente.id).first(),
        "antecedentes": db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente.id).first(),
        "habitos": db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente.id).first()
    }

# --- RUTAS DE PERSONAL ---
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {
        "doctores": db.query(models.Doctor).all(), 
        "enfermeras": db.query(models.Enfermera).all()
    }

@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)): 
    return crud.create_doctor(db, data)

@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)): 
    return crud.create_enfermera(db, data)

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.items(): setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    for key, value in data.items(): setattr(enfermera, key, value)
    db.commit()
    db.refresh(enfermera)
    return enfermera

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
