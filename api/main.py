from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

# Integridad de la base de datos [cite: 2026-02-03]
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

# RUTA DIRECTA PARA PACIENTE
@app.get("/get-paciente/{p_id}")
async def get_paciente(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"paciente": paciente}

# RUTA DIRECTA PARA GUARDAR P3 (Mapeo total de P1, P2, P3) [cite: 2026-02-11]
@app.post("/save-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # El campo 'coca' se recibe aquí validado por el esquema
        resultado = crud.upsert_p3(db, data.model_dump())
        return {"status": "success", "id": resultado.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
