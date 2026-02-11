import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# INICIALIZACIÓN DE DB (SQLite en /data/ para persistencia en Render)
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CONFIGURACIÓN CORS PARA COMUNICACIÓN GITHUB-RENDER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DEPENDE DE LA SESIÓN DE DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def status():
    return {"status": "online", "db": "connected"}

# --- REGISTRO DE PACIENTES (P0) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        ci_str = str(data.get("ci", ""))
        
        # Validación de duplicados para evitar error de integridad por 'unique=True'
        existente = db.query(models.Paciente).filter(models.Paciente.ci == ci_str).first()
        if existente:
            return existente
            
        db_obj = models.Paciente(
            nombre=str(data.get("nombre", "")),
            apellido=str(data.get("apellido", "")),
            ci=ci_str,
            codigo_paciente=str(data.get("codigo_paciente", ""))
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- PARTE 1: FILIACIÓN (FORZADO DE TIPOS PARA EVITAR ERROR 400) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Forzamos conversión a string de los campos que el HTML envía como número (edad)
        # para que coincidan con Column(String) del models.py
        db_obj = models.DeclaracionJurada(
            paciente_id=data.get("paciente_id"),
            edad=str(data.get("edad", "")),
            sexo=str(data.get("sexo", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "")),
            lugar_nacimiento=str(data.get("lugar_nacimiento", "")),
            domicilio=str(data.get("domicilio", "")),
            n_casa=str(data.get("n_casa", "")),
            zona_barrio=str(data.get("zona_barrio", "")),
            ciudad=str(data.get("ciudad", "")),
            pais=str(data.get("pais", "")),
            telefono=str(data.get("telefono", "")),
            estado_civil=str(data.get("estado_civil", "")),
            profesion_oficio=str(data.get("profesion_oficio", ""))
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Fallo en P1: {str(e)}")

# --- PARTE 2: ANTECEDENTES (22 CAMPOS) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.AntecedentesP2(
            paciente_id=data.get("paciente_id"),
            vista=str(data.get("vista", "")),
            auditivo=str(data.get("auditivo", "")),
            respiratorio=str(data.get("respiratorio", "")),
            cardio=str(data.get("cardio", "")),
            digestivos=str(data.get("digestivos", "")),
            sangre=str(data.get("sangre", "")),
            genitourinario=str(data.get("genitourinario", "")),
            sistema_nervioso=str(data.get("sistema_nervioso", "")),
            psiquiatricos=str(data.get("psiquiatricos", "")),
            osteomusculares=str(data.get("osteomusculares", "")),
            reumatologicos=str(data.get("reumatologicos", "")),
            dermatologicas=str(data.get("dermatologicas", "")),
            alergias=str(data.get("alergias", "")),
            cirugias=str(data.get("cirugias", "")),
            infecciones=str(data.get("infecciones", "")),
            acc_personales=str(data.get("acc_personales", "")),
            acc_trabajo=str(data.get("acc_trabajo", "")),
            medicamentos=str(data.get("medicamentos", "")),
            endocrino=str(data.get("endocrino", "")),
            familiares=str(data.get("familiares", "")),
            otros_especificos=str(data.get("otros_especificos", "")),
            generales=str(data.get("generales", ""))
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- PARTE 3: HÁBITOS (MANEJO DE TEXT/JSON) ---
@app.post("/declaraciones/p3/")
async def create_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.HabitosRiesgosP3(
            paciente_id=data.get("paciente_id"),
            fuma=str(data.get("fuma", "")),
            fuma_cantidad=str(data.get("fuma_cantidad", "")),
            alcohol=str(data.get("alcohol", "")),
            alcohol_frecuencia=str(data.get("alcohol_frecuencia", "")),
            drogas=str(data.get("drogas", "")),
            drogas_tipo=str(data.get("drogas_tipo", "")),
            coca=str(data.get("coca", "")),
            deporte=str(data.get("deporte", "")),
            deporte_detalle=str(data.get("deporte_detalle", "")),
            grupo_sanguineo=str(data.get("grupo_sanguineo", "")),
            historia_laboral=str(data.get("historia_laboral", "[]")),
            riesgos_expuestos=str(data.get("riesgos_expuestos", "[]")),
            observaciones=str(data.get("observaciones", ""))
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- LISTADO GENERAL ---
@app.get("/pacientes/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
