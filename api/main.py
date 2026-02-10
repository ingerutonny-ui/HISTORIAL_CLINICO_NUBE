from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

# Configuración de CORS para permitir la conexión desde GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creación de tablas en la base de datos (PostgreSQL en Render)
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTAS PARA PACIENTES ---

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

@app.post("/pacientes/")
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

# --- RUTAS PARA FORMULARIOS (P1, P2, P3) ---

@app.post("/filiacion/")
def guardar_p1(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_filiacion(db=db, filiacion=data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

@app.post("/declaraciones/p2/")
def guardar_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_antecedentes(db=db, antecedentes=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en P2: {str(e)}")

@app.post("/declaraciones/p3/")
def guardar_p3(data: schemas.HabitosP3Create, db: Session = Depends(get_db)):
    try:
        return crud.create_habitos(db=db, habitos=data)
    except Exception as e:
        # Este error 500 es el que capturamos si fallan las nuevas columnas
        raise HTTPException(status_code=500, detail=f"Error en P3: {str(e)}")
