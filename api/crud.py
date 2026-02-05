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

# --- NUEVAS FUNCIONES DE GESTIÓN ---
def get_paciente_by_codigo(db: Session, codigo: str):
    return db.query(models.Paciente).filter(models.Paciente.codigo_paciente == codigo).first()

def update_paciente(db: Session, codigo: str, datos_actualizados: schemas.PacienteCreate):
    db_paciente = get_paciente_by_codigo(db, codigo)
    if db_paciente:
        for key, value in datos_actualizados.model_dump().items():
            setattr(db_paciente, key, value)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    return None

def delete_paciente(db: Session, codigo: str):
    db_paciente = get_paciente_by_codigo(db, codigo)
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
        return True
    return False

# --- FUNCIONES DE DECLARACIONES EXISTENTES ---
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

def create_habitos_p3(db: Session, habitos: schemas.HabitosRiesgosP3Create):
    try:
        db_habitos = models.HabitosRiesgosP3(**habitos.model_dump())
        db.add(db_habitos)
        db.commit()
        db.refresh(db_habitos)
        return db_habitos
    except Exception as e:
        db.rollback()
        raise e
