from sqlalchemy.orm import Session
from . import models

# INGE: Función vital para que el CRUD encuentre al paciente por tu código (EJ: EH2345)
def get_paciente_by_codigo(db: Session, codigo: str):
    return db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()

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

# INGE: Modificado para soportar actualización (P2)
def upsert_p2(db: Session, data: dict):
    p_id = data.get("paciente_id")
    existente = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == p_id).first()
    if existente:
        for key, value in data.items():
            setattr(existente, key, value)
        db.commit()
        db.refresh(existente)
        return existente
    db_obj = models.AntecedentesP2(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# INGE: Modificado para soportar actualización (P3)
def upsert_p3(db: Session, data: dict):
    p_id = data.get("paciente_id")
    existente = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == p_id).first()
    if existente:
        for key, value in data.items():
            setattr(existente, key, value)
        db.commit()
        db.refresh(existente)
        return existente
    db_obj = models.HabitosRiesgosP3(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# INGE: Borrado físico del registro por su ID técnico
def delete_paciente(db: Session, paciente_id: int):
    db_obj = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
