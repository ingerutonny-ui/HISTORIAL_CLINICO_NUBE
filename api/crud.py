from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# --- OPERACIONES DE PACIENTE (P0) ---

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    try:
        db_paciente = models.Paciente(**paciente.model_dump())
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_pacientes(db: Session):
    return db.query(models.Paciente).all()

# --- OPERACIONES DE FORMULARIOS (P1, P2, P3) ---

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    try:
        data = filiacion.model_dump()
        # Mapeo forzado para asegurar compatibilidad con modelos de 75 líneas
        db_filiacion = models.DeclaracionJurada(**{
            k: v for k, v in data.items() 
            if hasattr(models.DeclaracionJurada, k)
        })
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error P1: {str(e)}")

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        data = antecedentes.model_dump()
        db_ant = models.AntecedentesP2(**{
            k: v for k, v in data.items() 
            if hasattr(models.AntecedentesP2, k)
        })
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error P2: {str(e)}")

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        data = habitos.model_dump()
        db_hab = models.HabitosRiesgosP3(**{
            k: v for k, v in data.items() 
            if hasattr(models.HabitosRiesgosP3, k)
        })
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error P3: {str(e)}")
