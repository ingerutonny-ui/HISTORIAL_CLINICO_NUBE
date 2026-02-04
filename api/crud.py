from sqlalchemy.orm import Session
from . import models, schemas

# --- LÓGICA PARA PACIENTES ---

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    """
    Crea un nuevo registro de paciente en la base de datos PostgreSQL.
    """
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# --- LÓGICA PARA DECLARACIÓN JURADA (PARTE 1) ---

def create_declaracion_p1(db: Session, declaracion: schemas.DeclaracionJuradaCreate):
    """
    Crea un nuevo registro de declaración jurada vinculada a un paciente.
    """
    db_declaracion = models.DeclaracionJurada(**declaracion.model_dump())
    db.add(db_declaracion)
    db.commit()
    db.refresh(db_declaracion)
    return db_declaracion
