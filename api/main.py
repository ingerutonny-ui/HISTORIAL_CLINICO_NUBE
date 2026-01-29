from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine, Base
from api import models, schemas

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Función para obtener la base de datos
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
    # 1. Crear la instancia del modelo con los datos recibidos
    nuevo_paciente = models.Paciente(
        nombres=paciente.nombres,
        apellidos=paciente.apellidos,
        documento_identidad=paciente.documento_identidad
    )
    
    # 2. Generar el código automático (ej: RA6855)
    nuevo_paciente.codigo_paciente = nuevo_paciente.generar_codigo()
    
    # 3. Guardar en PostgreSQL
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    
    return nuevo_paciente
