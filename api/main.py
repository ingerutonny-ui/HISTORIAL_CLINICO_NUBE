from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS para permitir la comunicación desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Rutas para Doctores ---
@app.post("/doctor/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data)

# --- Rutas para Enfermeras ---
@app.post("/enfermera/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data)

# --- Rutas para Pacientes ---
@app.post("/paciente/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data)

@app.post("/antecedentes_p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data)

@app.post("/habitos_p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data)

@app.delete("/paciente/{paciente_id}")
def borrar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado"}
