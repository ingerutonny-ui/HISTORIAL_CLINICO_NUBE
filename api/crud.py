from sqlalchemy.orm import Session
from . import models

# Crear un nuevo paciente
def crear_paciente(db: Session, nombre: str, apellido: str, dni: str, fecha_ingreso: str, codigo: str):
    nuevo_paciente = models.Paciente(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
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

# Consultar un paciente por DNI
def obtener_paciente_por_dni(db: Session, dni: str):
    return db.query(models.Paciente).filter(models.Paciente.dni == dni).first()
