from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    try:
        data = paciente.model_dump()
        db_paciente = models.Paciente(**data)
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
        raw_data = filiacion.model_dump()
        columnas = {c.name for c in models.DeclaracionJurada.__table__.columns}
        
        # Mapeo dinámico: solo guarda lo que existe en la tabla y lo convierte a string
        final_data = {}
        for k, v in raw_data.items():
            if k in columnas:
                if k == "paciente_id":
                    final_data[k] = int(v)
                else:
                    final_data[k] = str(v) if v is not None else ""

        db_filiacion = models.DeclaracionJurada(**final_data)
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error Crítico BD: {str(e)}")

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        raw_data = antecedentes.model_dump()
        db_ant = models.AntecedentesP2(paciente_id=int(raw_data.get("paciente_id")))
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        raw_data = habitos.model_dump()
        db_hab = models.HabitosRiesgosP3(paciente_id=int(raw_data.get("paciente_id")))
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
