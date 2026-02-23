from sqlalchemy.orm import Session
from . import models

def upsert_filiacion(db: Session, data: dict):
    obj = db.query(models.Paciente).filter(models.Paciente.id == data['id']).first()
    if obj:
        for k, v in data.items(): setattr(obj, k, v)
    else:
        obj = models.Paciente(**data)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def upsert_p2(db: Session, data: dict):
    obj = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == data['paciente_id']).first()
    if obj:
        for k, v in data.items(): setattr(obj, k, v)
    else:
        obj = models.AntecedentesP2(**data)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def upsert_p3(db: Session, data: dict):
    obj = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == data['paciente_id']).first()
    if obj:
        for k, v in data.items(): setattr(obj, k, v)
    else:
        obj = models.HabitosRiesgosP3(**data)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- NUEVAS FUNCIONES PARA PERSONAL MÉDICO ---

def upsert_doctor(db: Session, data: dict):
    """Busca por CI; si existe actualiza, si no crea un nuevo Doctor"""
    obj = db.query(models.Doctor).filter(models.Doctor.ci_doc == data['ci_doc']).first()
    if obj:
        for k, v in data.items(): setattr(obj, k, v)
    else:
        obj = models.Doctor(**data)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def upsert_enfermera(db: Session, data: dict):
    """Busca por CI; si existe actualiza, si no crea una nueva Enfermera"""
    obj = db.query(models.Enfermera).filter(models.Enfermera.ci_enfe == data['ci_enfe']).first()
    if obj:
        for k, v in data.items(): setattr(obj, k, v)
    else:
        obj = models.Enfermera(**data)
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
