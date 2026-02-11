from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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
    return {"status": "ok", "project": "HISTORIAL_CLINICO_NUBE", "storage": "DISK"}

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
    # Limpiamos el ID si viene como string vacío para evitar error de entero
    if "paciente_id" in data and not data["paciente_id"]:
        data.pop("paciente_id")
    db_filiacion = models.DeclaracionJurada(**data)
    db.add(db_filiacion)
    db.commit()
    db.refresh(db_filiacion)
    return db_filiacion
