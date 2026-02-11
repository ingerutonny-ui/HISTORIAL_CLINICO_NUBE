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
        f_nac = data.get("fecha_nacimiento") or data.get("fecha_nac") or ""
        
        db_filiacion = models.DeclaracionJurada(
            paciente_id=data.get("paciente_id"),
            edad=str(data.get("edad") or ""),
            sexo=str(data.get("sexo") or ""),
            fecha_nacimiento=str(f_nac),
            lugar_nacimiento=str(data.get("lugar_nacimiento") or ""),
            domicilio=str(data.get("domicilio") or ""),
            n_casa=str(data.get("n_casa") or ""),
            zona_barrio=str(data.get("zona_barrio") or ""),
            ciudad=str(data.get("ciudad") or ""),
            pais=str(data.get("pais") or ""),
            telefono=str(data.get("telefono") or ""),
            estado_civil=str(data.get("estado_civil") or ""),
            profesion_oficio=str(data.get("profesion_oficio") or "")
        )
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
        columnas = {c.name for c in models.AntecedentesP2.__table__.columns}
        db_ant = models.AntecedentesP2(**{k: v for k, v in data.items() if k in columnas})
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        data = habitos.model_dump()
        columnas = {c.name for c in models.HabitosRiesgosP3.__table__.columns}
        db_hab = models.HabitosRiesgosP3(**{k: v for k, v in data.items() if k in columnas})
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")
