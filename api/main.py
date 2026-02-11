import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# 1. INICIALIZACIÓN DE DB
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="HISTORIAL_CLINICO_NUBE",
    description="Sistema Robusto de Historias Clínicas",
    version="2.0.0"
)

# 2. CORS PARA GITHUB PAGES Y RENDER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. SESIÓN DE BASE DE DATOS
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def check_service():
    return {"status": "online", "mode": "Strict Learning Active"}

# --- RUTA 1: REGISTRO DE PACIENTES (P0) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        ci_str = str(data.get("ci", ""))
        
        # Evitar el error de CI duplicado (Unique Constraint)
        existente = db.query(models.Paciente).filter(models.Paciente.ci == ci_str).first()
        if existente:
            return existente
            
        db_obj = models.Paciente(
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            ci=ci_str,
            codigo_paciente=data.get("codigo_paciente")
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 2: PARTE 1 - FILIACIÓN (MAPEO TOLERANTE A ERRORES) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Mapeo que busca múltiples nombres posibles para evitar el Error 400
        db_obj = models.DeclaracionJurada(
            paciente_id=data.get("paciente_id"),
            edad=str(data.get("edad", "")),
            sexo=str(data.get("sexo", "")),
            fecha_nacimiento=str(data.get("fecha_nacimiento", "")),
            lugar_nacimiento=str(data.get("lugar_nacimiento", "")),
            domicilio=str(data.get("domicilio", data.get("domicilio_actual", ""))),
            n_casa=str(data.get("n_casa", data.get("n_casa_input", ""))),
            zona_barrio=str(data.get("zona_barrio", data.get("zona", ""))),
            ciudad=str(data.get("ciudad", "")),
            pais=str(data.get("pais", "")),
            telefono=str(data.get("telefono", data.get("celular", ""))),
            estado_civil=str(data.get("estado_civil", "")),
            profesion_oficio=str(data.get("profesion_oficio", data.get("profesion", "")))
        )
        
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "Filiación guardada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

# --- RUTA 3: PARTE 2 - ANTECEDENTES (TODOS LOS CAMPOS) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.AntecedentesP2(
            paciente_id=data.get("paciente_id"),
            vista=str(data.get("vista", "NORMAL")),
            auditivo=str(data.get("auditivo", "NORMAL")),
            respiratorio=str(data.get("respiratorio", "NORMAL")),
            cardio=str(data.get("cardio", "NORMAL")),
            digestivos=str(data.get("digestivos", "NORMAL")),
            sangre=str(data.get("sangre", "NORMAL")),
            genitourinario=str(data.get("genitourinario", "NORMAL")),
            sistema_nervioso=str(data.get("sistema_nervioso", "NORMAL")),
            psiquiatricos=str(data.get("psiquiatricos", "NORMAL")),
            osteomusculares=str(data.get("osteomusculares", "NORMAL")),
            reumatologicos=str(data.get("reumatologicos", "NORMAL")),
            dermatologicas=str(data.get("dermatologicas", "NORMAL")),
            alergias=str(data.get("alergias", "NORMAL")),
            cirugias=str(data.get("cirugias", "NORMAL")),
            infecciones=str(data.get("infecciones", "NORMAL")),
            acc_personales=str(data.get("acc_personales", "NORMAL")),
            acc_trabajo=str(data.get("acc_trabajo", "NORMAL")),
            medicamentos=str(data.get("medicamentos", "NORMAL")),
            endocrino=str(data.get("endocrino", "NORMAL")),
            familiares=str(data.get("familiares", "NORMAL")),
            otros_especificos=str(data.get("otros_especificos", "NORMAL")),
            generales=str(data.get("generales", "NORMAL"))
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 4: PARTE 3 - HÁBITOS (REFORZADO) ---
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

# --- RUTA 5: CONSULTA ---
@app.get("/pacientes/")
def list_all(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
