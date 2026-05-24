from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import create_doctor, create_enfermera
from . import models

# RECREACIÓN DE BASE DE DATOS (Ejecutar 1 vez para limpiar tipos)
Base.metadata.drop_all(bind=engine)
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

# ----------- BLOQUE P1 : FILIACION -----------
@app.get("/api/paciente-completo/{paciente_id}")
def obtener_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente, "filiacion": filiacion}

@app.post("/filiacion/")
def guardar_filiacion(data: dict, db: Session = Depends(get_db)):
    nueva = models.DeclaracionJurada(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

# ----------- BLOQUE P2: ANTECEDENTES -----------
@app.post("/p2/")
def guardar_p2(data: dict, db: Session = Depends(get_db)):
    nueva = models.AntecedentesP2(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/antecedentes/")
def guardar_antecedentes(data: dict, db: Session = Depends(get_db)):
    nueva = models.AntecedentesP2(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

# ----------- BLOQUE P3: HÁBITOS -----------
@app.post("/p3/")
def guardar_p3(data: dict, db: Session = Depends(get_db)):
    nueva = models.HabitosRiesgosP3(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/habitos/")
def guardar_habitos(data: dict, db: Session = Depends(get_db)):
    nueva = models.HabitosRiesgosP3(**data); db.add(nueva); db.commit(); db.refresh(nueva); return nueva

# ----------- GESTION PACIENTE (CRUD) -----------
@app.get("/paciente/{codigo}")
def buscar_paciente(codigo: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}

@app.post("/pacientes/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    nuevo = models.Paciente(**data)
    db.add(nuevo); db.commit(); db.refresh(nuevo); return nuevo

@app.put("/pacientes/{paciente_id}")
def actualizar_paciente(paciente_id: int, data: dict, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p: raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.items(): setattr(p, k, v)
    db.commit(); db.refresh(p); return p

@app.delete("/pacientes/{paciente_id}")
def borrar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(p); db.commit(); return {"message": "Eliminado"}

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.get("/paciente/{codigo}")
def buscar_paciente(codigo: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}


# ----------- FICHA MÉDICA -----------
@app.post("/ficha-oftalmo/")
def guardar_ficha_oftalmo(data: dict, db: Session = Depends(get_db)):
    nueva = models.FichaOftalmologica(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/ficha-psicologia/")
def guardar_ficha_psicologia(data: dict, db: Session = Depends(get_db)):
    nueva = models.FichaPsicologia(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/ficha-espirometria/")
def guardar_ficha_espirometria(data: dict, db: Session = Depends(get_db)):
    nueva = models.FichaEspirometria(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/ficha-electro/")
def guardar_ficha_electro(data: dict, db: Session = Depends(get_db)):
    nueva = models.FichaElectroencefalograma(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

@app.post("/declaracion/")
def guardar_declaracion(data: dict, db: Session = Depends(get_db)):
    nueva = models.DeclaracionJurada(**data)
    db.add(nueva); db.commit(); db.refresh(nueva); return nueva

# ----------- PERSONAL (CRUD) -----------
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {"doctores": db.query(models.Doctor).all(), "enfermeras": db.query(models.Enfermera).all()}

@app.get("/doctores/{id_doc}")
def obtener_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    return doctor

@app.get("/enfermeras/{id_enfe}")
def obtener_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    return enfermera

@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)): return create_doctor(db, data)

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.items(): setattr(doctor, key, value)
    db.commit(); db.refresh(doctor); return doctor

@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(doctor); db.commit(); return {"message": "Eliminado"}

@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)): return create_enfermera(db, data)

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    for key, value in data.items(): setattr(enfermera, key, value)
    db.commit(); db.refresh(enfermera); return enfermera

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    db.delete(enfermera); db.commit(); return {"message": "Eliminada"}
