from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Solo crea tablas si NO existen.
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

# --- LECTURA PARA CRUD Y REPORTES ---
@app.get("/api/paciente-completo/{paciente_id}")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    filiacion = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
    p2 = db.query(models.DeclaracionP2).filter(models.DeclaracionP2.paciente_id == paciente_id).first()
    p3 = db.query(models.DeclaracionP3).filter(models.DeclaracionP3.paciente_id == paciente_id).first()

    return {
        "paciente": paciente,
        "filiacion": filiacion if filiacion else {},
        "p2": p2 if p2 else {},
        "p3": p3 if p3 else {}
    }

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- ESCRITURA (GUARDADO) ---
@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.upsert_filiacion(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p2(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p3(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")
