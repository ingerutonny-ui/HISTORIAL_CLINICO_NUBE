from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# --- OPERACIONES DE PACIENTE ---

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def get_pacientes(db: Session):
    return db.query(models.Paciente).all()

# --- OPERACIONES DE FORMULARIOS ---

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    try:
        data = filiacion.model_dump()
        db_filiacion = models.DeclaracionJurada(**data)
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        data = antecedentes.model_dump()
        db_ant = models.AntecedentesP2(**data)
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        # Extraemos los datos del esquema validado
        data = habitos.model_dump()
        # Creamos la instancia del modelo con los nuevos campos de P3
        db_hab = models.HabitosRiesgosP3(**data)
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        # Aquí capturamos si hay inconsistencia con las columnas de models.py
        raise HTTPException(status_code=400, detail=f"Error en P3 (CRUD): {str(e)}")
