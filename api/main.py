from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esto asegura que las tablas existan en /data/historial.db
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/filiacion/")
def guardar_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    # Esta ruta coincide con declaracion_jurada_p1.html:97 de tu captura
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/pacientes/")
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)
