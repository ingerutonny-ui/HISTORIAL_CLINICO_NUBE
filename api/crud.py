from sqlalchemy.orm import Session
from . import models

# Crear un nuevo paciente
def crear_paciente(db: Session, nombre: str, apellido: str, ci: str, fecha_ingreso: str, codigo: str):
    nuevo_paciente = models.Paciente(
        nombre=nombre,
        apellido=apellido,
        ci=ci,
        fecha_ingreso=fecha_ingreso,
        codigo=codigo
    )
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente

# Consultar todos los pacientes
def obtener_pacientes(db: Session):
    return db.query(models.Paciente).all()

# Consultar un paciente por CI
def obtener_paciente_por_ci(db: Session, ci: str):
    return db.query(models.Paciente).filter(models.Paciente.ci == ci).first()
