from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Importaciones dinámicas para resolver el problema de la carpeta /api
try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

# Inicialización de tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS para producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTA UNIFICADA - Esto resuelve el 404 si el servidor busca con o sin prefijo
@app.post("/api/guardar-p3")
@app.post("/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Usamos model_dump() para Pydantic v2 (estándar actual) [cite: 2026-02-12]
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        print(f"Error en el servidor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Obtener paciente para la cabecera
@app.get("/api/paciente-completo/{p_id}")
@app.get("/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}
