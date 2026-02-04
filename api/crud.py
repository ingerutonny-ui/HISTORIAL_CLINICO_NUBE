from sqlalchemy.orm import Session
from . import models, schemas

def create_declaracion_p1(db: Session, declaracion: schemas.DeclaracionJuradaCreate):
    db_declaracion = models.DeclaracionJurada(**declaracion.model_dump())
    db.add(db_declaracion)
    db.commit()
    db.refresh(db_declaracion)
    return db_declaracion
