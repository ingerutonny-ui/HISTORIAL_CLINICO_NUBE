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

# Sincronización de base de datos PostgreSQL
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

# RUTA PARA EL BOTÓN P3 - Doble registro para asegurar compatibilidad con Render
@app.post("/api/guardar-p3")
@app.post("/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Usamos model_dump() para procesar todos los campos del schema P3
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "message": "P3 Guardado", "id": resultado.id}
    except Exception as e:
        print(f"Error técnico en P3: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/paciente-completo/{p_id}")
@app.get("/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}
