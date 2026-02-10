from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def get_pacientes(db: Session):
    return db.query(models.Paciente).all()

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    db_filiacion = models.DeclaracionJurada(**filiacion.model_dump())
    db.add(db_filiacion)
    db.commit()
    db.refresh(db_filiacion)
    return db_filiacion

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    db_ant = models.AntecedentesP2(**antecedentes.model_dump())
    db.add(db_ant)
    db.commit()
    db.refresh(db_ant)
    return db_ant

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        db_hab = models.HabitosRiesgosP3(**habitos.model_dump())
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error BD: {str(e)}")
