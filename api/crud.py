from sqlalchemy.orm import Session
from . import models, schemas

# Función para el botón CONSULTAR
def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

# Función para verificar si el paciente ya existe por CI
def get_paciente_by_ci(db: Session, ci: str):
    return db.query(models.Paciente).filter(models.Paciente.documento_identidad == ci).first()

# Función para el botón REGISTRAR
def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    # Creamos el objeto con los datos básicos que vienen del primer formulario
    db_paciente = models.Paciente(
        nombres=paciente.nombres,
        apellidos=paciente.apellidos,
        documento_identidad=paciente.documento_identidad,
        codigo_paciente=paciente.codigo_paciente
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente
