from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

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

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    try:
        data = filiacion.model_dump()
        columnas = {c.name for c in models.DeclaracionJurada.__table__.columns}
        # Limpieza dinámica: solo toma lo que la BD tiene definido
        db_filiacion = models.DeclaracionJurada(**{
            k: str(v) if v is not None else "" 
            for k, v in data.items() if k in columnas
        })
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error BD P1: {str(e)}")

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        data = antecedentes.model_dump()
        columnas = {c.name for c in models.AntecedentesP2.__table__.columns}
        db_ant = models.AntecedentesP2(**{
            k: str(v) if v is not None else "NORMAL" 
            for k, v in data.items() if k in columnas
        })
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error BD P2: {str(e)}")

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        data = habitos.model_dump()
        columnas = {c.name for c in models.HabitosRiesgosP3.__table__.columns}
        db_hab = models.HabitosRiesgosP3(**{
            k: str(v) if v is not None else "" 
            for k, v in data.items() if k in columnas
        })
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error BD P3: {str(e)}")
