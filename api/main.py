from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS PACIENTES ---
@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

# --- RUTAS ENFERMERA ---
@app.post("/enfermeras/")
async def save_enfermera(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    new_enfe = models.Enfermera(
        ci_enfe=data.get("ci_enfe"),
        appaterno_enfe=data.get("appaterno_enfe"),
        apmaterno_enfe=data.get("apmaterno_enfe"),
        nombre_enfe=data.get("nombre_enfe"),
        turno_enfe=data.get("turno_enfe"),
        edu_enfe=data.get("edu_enfe")
    )
    db.add(new_enfe)
    db.commit()
    db.refresh(new_enfe)
    return new_enfe

# --- RUTAS DOCTOR ---
@app.post("/doctores/")
async def save_doctor(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    new_doc = models.Doctor(
        ci_doc=data.get("ci_doc"),
        appaterno_doc=data.get("appaterno_doc"),
        apmaterno_doc=data.get("apmaterno_doc"),
        nombre_doc=data.get("nombre_doc"),
        turno_doc=data.get("turno_doc"),
        especialidad=data.get("especialidad")
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# --- OTRAS RUTAS (P1, P2, P3) ---
@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)

@app.get("/api/paciente-completo/{paciente_id}")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    return {
        "paciente": paciente,
        "filiacion": filiacion if filiacion else {},
        "p2": p2 if p2 else {},
        "p3": p3 if p3 else {}
    }

@app.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registro no existe.")
    return {"status": "success"}
