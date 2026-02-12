from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
from database import SessionLocal, engine

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PROYECTO HISTORIAL CLINICO NUBE")

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

# RUTA PARA EL VISOR (Lista básica)
@app.get("/pacientes/", response_model=list[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# RUTA PARA EL REPORTE (Detalle completo P1, P2, P3)
@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

# RUTA PARA GUARDAR
@app.post("/pacientes/", response_model=schemas.Paciente)
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente
