from sqlalchemy.orm import Session
from . import models, schemas

# Operaciones para Pacientes
def get_paciente_by_ci(db: Session, ci: str):
    return db.query(models.Paciente).filter(models.Paciente.documento_identidad == ci).first()

def get_pacientes(db: Session):
    return db.query(models.Paciente).all()

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Operaciones para Declaración Jurada
def create_declaracion_jurada_p1(db: Session, declaracion: schemas.DeclaracionJuradaCreate):
    db_declaracion = models.DeclaracionJurada(**declaracion.model_dump())
    db.add(db_declaracion)
    db.commit()
    db.refresh(db_declaracion)
    return db_declaracion

def get_declaraciones(db: Session):
    return db.query(models.DeclaracionJurada).all()
