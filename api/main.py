import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# 1. INICIALIZACIÓN DE BASE DE DATOS EN DISK PERSISTENTE
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE", version="1.0.0")

# 2. CONFIGURACIÓN DE SEGURIDAD CORS (CRUCIAL PARA GITHUB PAGES -> RENDER)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. DEPENDENCIA PARA LA SESIÓN DE DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. RUTA DE VERIFICACIÓN (HEALTH CHECK)
@app.get("/")
def root():
    return {
        "status": "online",
        "storage": "DISK_ACTIVE",
        "project": "HISTORIAL_CLINICO_NUBE",
        "check": "Full Mapping Active"
    }

# --- RUTA 1: REGISTRO DE PACIENTES (P0) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.Paciente(
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            ci=data.get("ci"),
            codigo_paciente=data.get("codigo_paciente")
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en Registro: {str(e)}")

# --- RUTA 2: PARTE 1 - FILIACIÓN (MAPEO EXPLÍCITO) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.DeclaracionJurada(
            paciente_id=data.get("paciente_id"),
            edad=str(data.get("edad")),
            sexo=data.get("sexo"),
            fecha_nacimiento=data.get("fecha_nacimiento"),
            lugar_nacimiento=data.get("lugar_nacimiento"),
            domicilio=data.get("domicilio"),
            n_casa=data.get("n_casa"),
            zona_barrio=data.get("zona_barrio"),
            ciudad=data.get("ciudad"),
            pais=data.get("pais"),
            telefono=data.get("telefono"),
            estado_civil=data.get("estado_civil"),
            profesion_oficio=data.get("profesion_oficio")
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "P1 Guardada correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

# --- RUTA 3: PARTE 2 - ANTECEDENTES (22 CAMPOS INDIVIDUALES) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.AntecedentesP2(
            paciente_id=data.get("paciente_id"),
            vista=data.get("vista"),
            auditivo=data.get("auditivo"),
            respiratorio=data.get("respiratorio"),
            cardio=data.get("cardio"),
            digestivos=data.get("digestivos"),
            sangre=data.get("sangre"),
            genitourinario=data.get("genitourinario"),
            sistema_nervioso=data.get("sistema_nervioso"),
            psiquiatricos=data.get("psiquiatricos"),
            osteomusculares=data.get("osteomusculares"),
            reumatologicos=data.get("reumatologicos"),
            dermatologicas=data.get("dermatologicas"),
            alergias=data.get("alergias"),
            cirugias=data.get("cirugias"),
            infecciones=data.get("infecciones"),
            acc_personales=data.get("acc_personales"),
            acc_trabajo=data.get("acc_trabajo"),
            medicamentos=data.get("medicamentos"),
            endocrino=data.get("endocrino"),
            familiares=data.get("familiares"),
            otros_especificos=data.get("otros_especificos"),
            generales=data.get("generales")
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "P2 Guardada (22 campos)"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

# --- RUTA 4: PARTE 3 - HÁBITOS Y RIESGOS ---
@app.post("/declaraciones/p3/")
async def create_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.HabitosRiesgosP3(
            paciente_id=data.get("paciente_id"),
            fuma=data.get("fuma"),
            fuma_cantidad=data.get("fuma_cantidad"),
            alcohol=data.get("alcohol"),
            alcohol_frecuencia=data.get("alcohol_frecuencia"),
            drogas=data.get("drogas"),
            drogas_tipo=data.get("drogas_tipo"),
            coca=data.get("coca"),
            deporte=data.get("deporte"),
            deporte_detalle=data.get("deporte_detalle"),
            grupo_sanguineo=data.get("grupo_sanguineo"),
            historia_laboral=data.get("historia_laboral"),
            riesgos_expuestos=data.get("riesgos_expuestos"),
            observaciones=data.get("observaciones")
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "P3 Guardada Final"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")

# --- RUTA 5: CONSULTA PARA LISTADO ---
@app.get("/pacientes/")
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
