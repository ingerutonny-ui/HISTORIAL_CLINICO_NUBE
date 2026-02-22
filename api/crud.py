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
