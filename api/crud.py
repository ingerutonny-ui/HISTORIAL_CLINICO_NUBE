from sqlalchemy.orm import Session
from . import models, schemas

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    try:
        db_paciente = models.Paciente(**paciente.model_dump())
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except Exception as e:
        db.rollback()
        raise e

def create_declaracion_p1(db: Session, declaracion: schemas.DeclaracionJuradaCreate):
    try:
        db_declaracion = models.DeclaracionJurada(**declaracion.model_dump())
        db.add(db_declaracion)
        db.commit()
        db.refresh(db_declaracion)
        return db_declaracion
    except Exception as e:
        db.rollback()
        raise e

def create_antecedentes_p2(db: Session, antecedentes: schemas.AntecedentesP2Create):
    try:
        db_antecedentes = models.AntecedentesP2(**antecedentes.model_dump())
        db.add(db_antecedentes)
        db.commit()
        db.refresh(db_antecedentes)
        return db_antecedentes
    except Exception as e:
        db.rollback()
        raise e
