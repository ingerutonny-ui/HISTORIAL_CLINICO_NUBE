from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración Maestra de CORS
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
def read_root():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# RUTA PARA LISTA DE PACIENTES (Soluciona "Error al cargar")
@app.get("/pacientes/")
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# RUTA PARA P1 (Soluciona el 404 de tus capturas)
@app.post("/filiacion/")
def save_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.DeclaracionJurada(**data.dict())
        db.add(new_entry)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RUTA PARA P2 (Soluciona el 500/CORS de tus capturas)
@app.post("/declaraciones/p2/")
def save_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.AntecedentesP2(**data.dict())
        db.add(new_entry)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
