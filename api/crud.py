from sqlalchemy.orm import Session
from . import models, schemas

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    try:
        # Usamos model_dump() para convertir los datos del schema a diccionario
        db_paciente = models.Paciente(**paciente.model_dump())
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except Exception as e:
        db.rollback()
        raise e

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
