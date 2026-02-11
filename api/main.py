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
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok", "storage": "DISK", "step": "P2_ACTIVE"}

@app.get("/pacientes/")
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    db_paciente = models.Paciente(**data)
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    allowed = [c.key for c in models.DeclaracionJurada.__table__.columns]
    filtered = {k: v for k, v in data.items() if k in allowed}
    db_obj = models.DeclaracionJurada(**filtered)
    db.add(db_obj)
    db.commit()
    return {"status": "success"}

# NUEVA RUTA PARA SOLUCIONAR EL ERROR 404 DE LA P2
@app.post("/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        # Guardamos todo el bloque de antecedentes como un JSON string para no perder nada
        paciente_id = data.get("paciente_id")
        db_p2 = models.AntecedentesP2(
            paciente_id=paciente_id,
            datos_antecedentes=json.dumps(data)
        )
        db.add(db_p2)
        db.commit()
        return {"status": "success", "message": "Antecedentes P2 guardados"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
