from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

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

# PRUEBA DE VIDA: Entra a https://historial-clinico-936s.onrender.com/api/test
@app.get("/api/test")
async def test():
    return {"mensaje": "El servidor responde correctamente"}

@app.get("/api/pacientes/{p_id}")
async def get_paciente(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@app.post("/api/save-p1")
async def save_p1(data: schemas.DeclaracionJuradaBase, db: Session = Depends(get_db)):
    try:
        return crud.upsert_filiacion(db, data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-p2")
async def save_p2(data: schemas.AntecedentesP2Base, db: Session = Depends(get_db)):
    try:
        return crud.upsert_p2(db, data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RUTA REFORZADA
@app.post("/api/registrar-p3")
async def registrar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # IMPORTANTE: Asegúrate que en crud.py exista la función upsert_p3
        resultado = crud.upsert_p3(db, data.model_dump())
        return resultado
    except Exception as e:
        logging.error(f"ERROR EN P3: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
