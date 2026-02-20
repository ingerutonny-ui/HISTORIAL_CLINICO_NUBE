from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Intentar crear tablas al iniciar
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    print(f"Error creando tablas: {e}")

app = FastAPI()

# Configuración de CORS corregida para evitar el error de la captura
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

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

@app.post("/enfermeras/")
async def save_enfermera(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_enfermera(db, data)

@app.post("/doctores/")
async def save_doctor(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_doctor(db, data)

# --- RUTAS DE EDICIÓN Y CONSULTA ---
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
