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

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

# --- RUTAS PARTE 2 (CON PUT PARA EDICIÓN) ---
@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

@app.put("/declaraciones/p2/{paciente_id}")
async def update_p2(paciente_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

# --- RUTAS PARTE 3 (CON PUT PARA EDICIÓN) ---
@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)

@app.put("/declaraciones/p3/{paciente_id}")
async def update_p3(paciente_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)

@app.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registro no existe.")
    return {"status": "success"}
