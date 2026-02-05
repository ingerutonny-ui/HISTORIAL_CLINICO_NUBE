from sqlalchemy.orm import Session
from . import models, schemas

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    db_filiacion = models.DeclaracionJurada(**filiacion.dict())
    db.add(db_filiacion)
    db.commit()
    db.refresh(db_filiacion)
    return db_filiacion

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    # Esta función ahora guarda correctamente los 22 campos enviados desde P2
    db_ante = models.AntecedentesP2(**antecedentes.dict())
    db.add(db_ante)
    db.commit()
    db.refresh(db_ante)
    return db_ante

def create_habitos(db: Session, habitos: schemas.HabitosCreate):
    db_hab = models.HabitosRiesgosP3(**habitos.dict())
    db.add(db_hab)
    db.commit()
    db.refresh(db_hab)
    return db_hab

def get_historial_completo(db: Session, paciente_id: int):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    antecedentes = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    habitos = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    return {
        "paciente": paciente,
        "filiacion": filiacion,
        "antecedentes": antecedentes,
        "habitos": habitos
    }
