from sqlalchemy.orm import Session
from . import models, schemas

# --- GESTIÓN DE PACIENTES ---
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

# --- GESTIÓN DE FILIACIÓN (PARTE 1) ---
def create_filiacion(db: Session, filiacion: schemas.FiliacionCreate):
    try:
        # Verificar si ya existe para actualizar o crear nuevo
        db_filiacion = db.query(models.DeclaracionJurada).filter(
            models.DeclaracionJurada.paciente_id == filiacion.paciente_id
        ).first()
        
        if db_filiacion:
            for key, value in filiacion.model_dump().items():
                setattr(db_filiacion, key, value)
        else:
            db_filiacion = models.DeclaracionJurada(**filiacion.model_dump())
            db.add(db_filiacion)
            
        db.commit()
        db.refresh(db_filiacion)
        return db_filiacion
    except Exception as e:
        db.rollback()
        raise e

# --- GESTIÓN DE ANTECEDENTES (PARTE 2) ---
def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        db_ant = db.query(models.AntecedentesP2).filter(
            models.AntecedentesP2.paciente_id == antecedentes.paciente_id
        ).first()
        
        if db_ant:
            for key, value in antecedentes.model_dump().items():
                setattr(db_ant, key, value)
        else:
            db_ant = models.AntecedentesP2(**antecedentes.model_dump())
            db.add(db_ant)
            
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise e

# --- GESTIÓN DE HÁBITOS (PARTE 3) ---
def create_habitos(db: Session, habitos: schemas.HabitosCreate):
    try:
        db_hab = db.query(models.HabitosRiesgosP3).filter(
            models.HabitosRiesgosP3.paciente_id == habitos.paciente_id
        ).first()
        
        if db_hab:
            for key, value in habitos.model_dump().items():
                setattr(db_hab, key, value)
        else:
            db_hab = models.HabitosRiesgosP3(**habitos.model_dump())
            db.add(db_hab)
            
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise e

# --- OBTENCIÓN DE HISTORIAL COMPLETO ---
def get_historial_completo(db: Session, paciente_id: int):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        return None
    
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    antecedentes = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    habitos = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()
    
    return {
        "paciente": paciente,
        "filiacion": filiacion,
        "antecedentes": antecedentes,
        "habitos": habitos
    }
