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
    db_paciente = models.Paciente(**paciente.dict())
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
    db_declaracion = models.DeclaracionJurada(**declaracion.dict())
    db.add(db_declaracion)
    db.commit()
    db.refresh(db_declaracion)
    return db_declaracion
