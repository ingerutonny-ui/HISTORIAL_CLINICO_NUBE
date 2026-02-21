from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Importación absoluta para garantizar que encuentre los archivos en la subcarpeta /api
try:
    import models, schemas, crud
    from database import SessionLocal, engine
except ImportError:
    from . import models, schemas, crud
    from .database import SessionLocal, engine

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

# RUTA PARA EL BOTÓN DE P3
@app.post("/api/guardar-p3")
@app.post("/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Se usa model_dump() para compatibilidad total con los Schemas que me pasaste
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RUTA PARA DATOS DEL PACIENTE (CABECERA)
@app.get("/api/paciente-completo/{p_id}")
@app.get("/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}
