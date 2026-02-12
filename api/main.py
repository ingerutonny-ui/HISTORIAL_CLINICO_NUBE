from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

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

@app.get("/pacientes/{paciente_id}")
def get_paciente_unificado(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    filiacion = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
    # Retornamos todo en un solo objeto para facilitar el mapeo
    return {
        "paciente": paciente,
        "filiacion": filiacion if filiacion else {}
    }

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- RUTAS DE GUARDADO (P1, P2, P3) ---
@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)
