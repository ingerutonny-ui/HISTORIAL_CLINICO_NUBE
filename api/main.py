from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

# Sincronización de modelos con PostgreSQL [cite: 2026-02-03]
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTA PARA DATOS DE CABECERA
@app.get("/get-paciente/{p_id}")
async def get_paciente(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}

# RUTA POST SIN /API/ PARA EVITAR ERROR 404
@app.post("/save-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # El campo 'coca' se mapea aquí directamente del esquema
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
