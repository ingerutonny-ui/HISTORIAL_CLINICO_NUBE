from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CONFIGURACIÓN CORS INTEGRAL [cite: 2026-02-03]
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

# TÉCNICA RUTAS ESPEJO PARA P1, P2 Y P3
@app.get("/api/pacientes/{p_id}")
@app.get("/api/get-paciente/{p_id}")
async def get_paciente(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    # Devolvemos el objeto directamente para compatibilidad total
    return paciente

# RUTA DE GUARDADO P3 CON MAPEO COMPLETO
@app.post("/api/save-p3")
@app.post("/api/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
