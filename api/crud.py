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
        db_filiacion = models.DeclaracionJurada(
            paciente_id=int(data.get("paciente_id")),
            edad=str(data.get("edad") or ""),
            sexo=str(data.get("sexo") or ""),
            fecha_nacimiento=str(data.get("fecha_nacimiento") or ""),
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
        raise HTTPException(status_code=400, detail=f"Fallo P1: {str(e)}")

def create_antecedentes(db: Session, antecedentes: schemas.AntecedentesCreate):
    try:
        data = antecedentes.model_dump()
        # Mapeo completo para P2
        db_ant = models.AntecedentesP2(
            paciente_id=int(data.get("paciente_id")),
            vista=str(data.get("vista") or "NORMAL"),
            auditivo=str(data.get("auditivo") or "NORMAL"),
            respiratorio=str(data.get("respiratorio") or "NORMAL"),
            cardio=str(data.get("cardio") or "NORMAL"),
            digestivos=str(data.get("digestivos") or "NORMAL"),
            sangre=str(data.get("sangre") or "NORMAL"),
            genitourinario=str(data.get("genitourinario") or "NORMAL"),
            sistema_nervioso=str(data.get("sistema_nervioso") or "NORMAL"),
            psiquiatricos=str(data.get("psiquiatricos") or "NORMAL"),
            osteomusculares=str(data.get("osteomusculares") or "NORMAL"),
            reumatologicos=str(data.get("reumatologicos") or "NORMAL"),
            dermatologicas=str(data.get("dermatologicas") or "NORMAL"),
            alergias=str(data.get("alergias") or "NORMAL"),
            cirugias=str(data.get("cirugias") or "NORMAL"),
            infecciones=str(data.get("infecciones") or "NORMAL"),
            acc_personales=str(data.get("acc_personales") or "NORMAL"),
            acc_trabajo=str(data.get("acc_trabajo") or "NORMAL"),
            medicamentos=str(data.get("medicamentos") or "NORMAL"),
            endocrino=str(data.get("endocrino") or "NORMAL"),
            familiares=str(data.get("familiares") or "NORMAL"),
            otros_especificos=str(data.get("otros_especificos") or "NORMAL"),
            generales=str(data.get("generales") or "NORMAL")
        )
        db.add(db_ant)
        db.commit()
        db.refresh(db_ant)
        return db_ant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Fallo P2: {str(e)}")

def create_habitos(db: Session, habitos: schemas.HabitosP3Create):
    try:
        data = habitos.model_dump()
        # Mapeo completo para P3
        db_hab = models.HabitosRiesgosP3(
            paciente_id=int(data.get("paciente_id")),
            fuma=str(data.get("fuma") or "NO"),
            fuma_cantidad=str(data.get("fuma_cantidad") or ""),
            alcohol=str(data.get("alcohol") or "NO"),
            alcohol_frecuencia=str(data.get("alcohol_frecuencia") or ""),
            drogas=str(data.get("drogas") or "NO"),
            drogas_tipo=str(data.get("drogas_tipo") or ""),
            coca=str(data.get("coca") or "NO"),
            deporte=str(data.get("deporte") or "NO"),
            deporte_detalle=str(data.get("deporte_detalle") or ""),
            grupo_sanguineo=str(data.get("grupo_sanguineo") or ""),
            historia_laboral=str(data.get("historia_laboral") or "[]"),
            riesgos_expuestos=str(data.get("riesgos_expuestos") or "[]"),
            observaciones=str(data.get("observaciones") or "SIN OBSERVACIONES")
        )
        db.add(db_hab)
        db.commit()
        db.refresh(db_hab)
        return db_hab
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Fallo P3: {str(e)}")
