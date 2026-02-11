from sqlalchemy.orm import Session
from . import models

def get_paciente_by_ci(db: Session, ci: str):
    return db.query(models.Paciente).filter(models.Paciente.ci == ci).first()

def create_paciente(db: Session, data: dict):
    db_obj = models.Paciente(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def upsert_filiacion(db: Session, data: dict):
    p_id = data.get("paciente_id")
    existente = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == p_id).first()
    if existente:
        for key, value in data.items():
            setattr(existente, key, value)
        db.commit()
        db.refresh(existente)
        return existente
    db_obj = models.DeclaracionJurada(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def create_p2(db: Session, data: dict):
    db_obj = models.AntecedentesP2(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def create_p3(db: Session, data: dict):
    db_obj = models.HabitosRiesgosP3(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
