from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
from . import models, database

database.Base.metadata.create_all(bind=database.engine)

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
    try: yield db
    finally: db.close()

@app.get("/")
def root():
    return {"status": "ok", "project": "HISTORIAL_CLINICO_NUBE", "step": "P3_READY"}

@app.get("/pacientes/")
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- ENDPOINTS EXISTENTES P1 Y P2 ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    db_obj = models.Paciente(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    cols = [c.key for c in models.DeclaracionJurada.__table__.columns]
    filtered = {k: v for k, v in data.items() if k in cols}
    db_obj = models.DeclaracionJurada(**filtered)
    db.add(db_obj)
    db.commit()
    return {"status": "success"}

@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    db_p2 = models.AntecedentesP2(paciente_id=data.get("paciente_id"), datos_json=json.dumps(data))
    db.add(db_p2)
    db.commit()
    return {"status": "success"}

# --- NUEVO ENDPOINT PARA P3 ---
@app.post("/declaraciones/p3/")
async def create_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        p_id = data.get("paciente_id")
        # Guardamos todos los campos (hábitos, laboral, riesgos) en un solo Text
        db_p3 = models.HabitosRiesgosP3(
            paciente_id=p_id,
            datos_p3=json.dumps(data)
        )
        db.add(db_p3)
        db.commit()
        return {"status": "success", "message": "P3 Guardada"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
