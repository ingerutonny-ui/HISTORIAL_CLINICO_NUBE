from sqlalchemy.orm import Session
from . import models, schemas

# --- OPERACIONES PARA PACIENTES ---
def get_paciente(db: Session, paciente_id: int):
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()

def get_paciente_by_ci(db: Session, ci: str):
    return db.query(models.Paciente).filter(models.Paciente.documento_identidad == ci).first()

def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    # Convertimos el esquema a diccionario para insertar en la base de datos
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# --- OPERACIONES PARA DECLARACIÓN JURADA ---
def get_declaraciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeclaracionJurada).offset(skip).limit(limit).all()

def get_declaracion_by_paciente(db: Session, paciente_id: int):
    return db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()

def create_declaracion_jurada(db: Session, declaracion: schemas.DeclaracionJuradaCreate):
    # Usamos model_dump() (que reemplaza al antiguo .dict()) para capturar 
    # los 17 riesgos, hábitos e historia laboral de un solo golpe.
    db_declaracion = models.DeclaracionJurada(**declaracion.model_dump())
    db.add(db_declaracion)
    db.commit()
    db.refresh(db_declaracion)
    return db_declaracion
