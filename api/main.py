from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Configuración de redirección de barras automática
app = FastAPI(redirect_slashes=True)

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

# --- RUTAS DE DOCTORES (UNIFICADAS) ---
@app.post("/doctor")
@app.post("/doctor/")
async def save_doctor(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_doctor(db, data)

@app.get("/doctores")
@app.get("/doctores/")
def list_doctores(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

# --- RUTAS DE ENFERMERAS (UNIFICADAS) ---
@app.post("/enfermera")
@app.post("/enfermera/")
async def save_enfermera(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_enfermera(db, data)

@app.get("/enfermeras")
@app.get("/enfermeras/")
def list_enfermeras(db: Session = Depends(get_db)):
    return db.query(models.Enfermera).all()

# --- PACIENTES Y REPORTES (TRILLIZOS P1, P2, P3) ---

@app.get("/pacientes")
@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes")
@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

# Mapeo de Filiación (P1)
@app.post("/filiacion")
@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

# Mapeo de Antecedentes (P2) - Aquí estaba el posible 404
@app.post("/p2")
@app.post("/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

# Mapeo de Hábitos (P3)
@app.post("/p3")
@app.post("/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)

# OBTENCIÓN COMPLETA PARA EL REPORTE HTML
@app.get("/api/paciente-completo/{paciente_id}")
@app.get("/api/paciente-completo/{paciente_id}/")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Buscamos en las tres tablas de los trillizos
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    
    return {
        "paciente": paciente, 
        "filiacion": filiacion or {}, 
        "p2": p2 or {}, 
        "p3": p3 or {}
    }
