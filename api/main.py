from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

try:
    models.Base.metadata.create_all(bind=engine)
    print("Base de datos conectada y tablas verificadas.")
except Exception as e:
    print(f"Error crítico de conexión: {e}")

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

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

@app.get("/")
def read_root():
    return {"status": "ONLINE", "database": "CONNECTED"}

# --- RUTAS DE PACIENTES (EXTENDIDAS) ---

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_paciente(db=db, paciente=paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes/{codigo}", response_model=schemas.Paciente)
def read_paciente_por_codigo(codigo: str, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_codigo(db, codigo=codigo)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

@app.put("/pacientes/{codigo}", response_model=schemas.Paciente)
def update_paciente(codigo: str, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, codigo=codigo, datos_actualizados=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="No se pudo actualizar: Paciente no encontrado")
    return db_paciente

@app.delete("/pacientes/{codigo}")
def delete_paciente(codigo: str, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, codigo=codigo)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: Paciente no encontrado")
    return {"message": f"Paciente {codigo} eliminado exitosamente"}

# --- RUTAS DE DECLARACIONES (GUARDADO) ---

@app.post("/declaraciones/p1/", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_declaracion_p1(db=db, declaracion=declaracion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p2/", response_model=schemas.AntecedentesP2)
def save_p2(antecedentes: schemas.AntecedentesP2Create, db: Session = Depends(get_db)):
    try:
        return crud.create_antecedentes_p2(db=db, antecedentes=antecedentes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p3/", response_model=schemas.HabitosRiesgosP3)
def save_p3(habitos: schemas.HabitosRiesgosP3Create, db: Session = Depends(get_db)):
    try:
        return crud.create_habitos_p3(db=db, habitos=habitos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RUTA DE CONSULTA INTEGRAL (PARA EL VISOR DE HISTORIAL) ---

@app.get("/historial-completo/{paciente_id}")
def get_historial_completo(paciente_id: int, db: Session = Depends(get_db)):
    """
    Busca todas las partes de la declaración jurada de un paciente 
    y las devuelve en un solo objeto.
    """
    p1 = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    
    return {
        "p1": p1,
        "p2": p2,
        "p3": p3
    }
