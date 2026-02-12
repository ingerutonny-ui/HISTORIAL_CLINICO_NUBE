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

@app.get("/")
def health_check():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS DE PACIENTES ---
@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.get("/pacientes/{paciente_id}")
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

# --- RUTAS DE SECCIONES SEPARADAS ---
@app.get("/filiacion/{paciente_id}")
def get_filiacion(paciente_id: int, db: Session = Depends(get_db)):
    f = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
    return f if f else {}

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_p2(db, data)

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_p3(db, data)
