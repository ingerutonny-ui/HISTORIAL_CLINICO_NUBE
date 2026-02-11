from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# Crear tablas e iniciar conexión al DISK
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

# RUTA PARA EL BOTÓN "CONSULTAR BASE DE DATOS"
@app.get("/pacientes/")
def get_all_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"status": "ok", "storage": "DISK", "database": "connected"}

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
    db_filiacion = models.DeclaracionJurada(**data)
    db.add(db_filiacion)
    db.commit()
    db.refresh(db_filiacion)
    return db_filiacion
