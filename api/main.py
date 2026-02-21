from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import schemas, crud, models
from .database import SessionLocal, engine

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.post("/api/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Usamos tu función upsert_p3 que ya existe en crud.py
        resultado = crud.upsert_p3(db, data.dict())
        return {"status": "success", "message": "P3 Sincronizado en PostgreSQL", "id": resultado.id}
    except Exception as e:
        print(f"Error en P3: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}
