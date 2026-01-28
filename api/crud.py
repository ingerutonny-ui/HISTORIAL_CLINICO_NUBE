from sqlalchemy.orm import Session
from . import models, schemas

def generar_codigo_paciente(db: Session, nombre: str, apellido: str):
    # 1. Extraer iniciales en mayúsculas
    iniciales = (nombre[0] + apellido[0]).upper()
    
    # 2. Contar cuántos pacientes existen para asignar el siguiente número
    conteo = db.query(models.Paciente).count()
    numero_secuencial = str(conteo + 1).zfill(3) # Ejemplo: 001, 002
    
    return f"{iniciales}{numero_secuencial}"

def crear_paciente(db: Session, paciente: schemas.PacienteCreate):
    # Generamos el código único antes de insertar
    codigo = generar_codigo_paciente(db, paciente.nombre, paciente.apellido)
    
    db_paciente = models.Paciente(
        codigo_paciente=codigo,
        nombre=paciente.nombre,
        apellido=paciente.apellido,
        historia_clinica=paciente.historia_clinica
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def obtener_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()
