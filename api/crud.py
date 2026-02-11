from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    try:
        # Convierte lo que sea que llegue en un diccionario y lo guarda
        db_paciente = models.Paciente(**paciente.model_dump())
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    try:
        # Forzamos el guardado de los datos que vienen del formulario
        db_filiacion = models.DeclaracionJurada(**filiacion.model_dump())
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")
