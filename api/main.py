from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creación de tablas al iniciar el servicio
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    print(f"Error al crear tablas: {e}")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    try:
        return crud.get_pacientes(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pacientes/")
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_paciente(db=db, paciente=paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/filiacion/")
def guardar_p1(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    # Verificación estricta del paciente_id antes de intentar guardar
    if not data.paciente_id or data.paciente_id <= 0:
        raise HTTPException(
            status_code=422, 
            detail="Error: El ID del paciente no es válido o no se recibió."
        )
    try:
        return crud.create_filiacion(db=db, filiacion=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en BD al guardar P1: {str(e)}")

@app.post("/declaraciones/p2/")
def guardar_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_antecedentes(db=db, antecedentes=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en BD al guardar P2: {str(e)}")

@app.post("/declaraciones/p3/")
def guardar_p3(data: schemas.HabitosP3Create, db: Session = Depends(get_db)):
    try:
        return crud.create_habitos(db=db, habitos=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en BD al guardar P3: {str(e)}")
