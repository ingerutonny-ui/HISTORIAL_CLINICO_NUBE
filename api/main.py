from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Importación robusta para la estructura de carpetas en Render
try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

# Inicialización de PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración CORS abierta para evitar bloqueos entre GitHub y Render
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

# RUTA PARA RECUPERAR PACIENTE (REPARA EL "CARGANDO...")
@app.get("/paciente-completo/{p_id}")
@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}

# RUTA PARA GUARDAR P3
@app.post("/guardar-p3")
@app.post("/api/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Se procesan todos los campos de P1, P2 y P3 mapeados [cite: 2026-02-11]
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
