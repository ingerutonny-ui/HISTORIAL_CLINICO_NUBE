from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api import models, schemas, crud
from api.database import SessionLocal, engine

# Creamos las tablas en Render automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CONFIGURACIÓN CLAVE: Esto permite que tu HTML de GitHub se conecte a Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite conexiones desde cualquier lugar por ahora
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pacientes/", response_model=schemas.Paciente)
def crear_nuevo_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    # Aquí llamamos a la lógica para guardar y generar el código (RA1234)
    return crud.crear_paciente(db=db, paciente=paciente)

@app.get("/")
def inicio():
    return {"mensaje": "Servidor de HISTORIAL_CLINICO_NUBE funcionando"}
