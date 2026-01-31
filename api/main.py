from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine, Base
from api import models, schemas

# Crear tablas en PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI()

# SEGURIDAD TOTAL: Esto permite que tu formulario de GitHub se conecte sin errores
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
    return {"message": "API HISTORIAL_CLINICO_NUBE en linea"}

@app.post("/pacientes/", response_model=schemas.PacienteResponse)
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    nuevo_paciente = models.Paciente(
        nombres=paciente.nombres,
        apellidos=paciente.apellidos,
        documento_identidad=paciente.documento_identidad
    )
    nuevo_paciente.codigo_paciente = nuevo_paciente.generar_codigo()
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente

@app.get("/pacientes/", response_model=list[schemas.PacienteResponse])
def obtener_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
