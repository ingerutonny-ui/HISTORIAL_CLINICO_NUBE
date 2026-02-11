import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# 1. INICIALIZACIÓN DE LA BASE DE DATOS
# Asegura que las tablas en el models.py se creen en Render
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="HISTORIAL_CLINICO_NUBE",
    description="Sistema de Gestión de Historias Clínicas - Modo Aprender Activo",
    version="1.5.0"
)

# 2. CONFIGURACIÓN DE SEGURIDAD CORS
# Permite que el Frontend en GitHub se comunique con el Backend en Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. GESTIÓN DE SESIÓN DE BASE DE DATOS
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTA DE VERIFICACIÓN ---
@app.get("/")
def home():
    return {
        "status": "online",
        "database": "connected",
        "project": "HISTORIAL_CLINICO_NUBE",
        "mode": "learning_strict"
    }

# --- RUTA 1: REGISTRO DE PACIENTES (P0) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        ci_recibido = str(data.get("ci"))
        
        # SOLUCIÓN AL ERROR 400: Verificar si el CI ya existe antes de intentar guardar
        # Esto permite que si la P1 falló, el usuario pueda reintentar sin romper el CI Unique
        paciente_existente = db.query(models.Paciente).filter(models.Paciente.ci == ci_recibido).first()
        
        if paciente_existente:
            print(f"Paciente ya registrado con CI: {ci_recibido}. Retornando registro existente.")
            return paciente_existente
            
        db_obj = models.Paciente(
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            ci=ci_recibido,
            codigo_paciente=data.get("codigo_paciente")
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        print(f"Error en Registro Paciente: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en P0: {str(e)}")

# --- RUTA 2: PARTE 1 - FILIACIÓN (PROCESAMIENTO DETALLADO) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Mapeo explícito para asegurar que cada campo del models.py se llene correctamente
        # Se usa str() para garantizar compatibilidad con los campos String del modelo
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
        return {"status": "success", "message": "Filiación guardada correctamente", "next_step": "P2"}
    except Exception as e:
        db.rollback()
        print(f"Error Crítico en Filiación: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

# --- RUTA 3: PARTE 2 - ANTECEDENTES (LOS 22 CAMPOS MÉDICOS) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Mapeo uno a uno de los 22 campos definidos en el models.py
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
        return {"status": "success", "message": "Antecedentes P2 registrados"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

# --- RUTA 4: PARTE 3 - HÁBITOS Y RIESGOS (DATOS COMPLEJOS) ---
@app.post("/declaraciones/p3/")
async def create_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Los campos historia_laboral y riesgos_expuestos se guardan como texto (JSON)
        # según la definición de Column(Text) en models.py
        db_obj = models.HabitosRiesgosP3(
            paciente_id=data.get("paciente_id"),
            fuma=str(data.get("fuma", "NO")),
            fuma_cantidad=str(data.get("fuma_cantidad", "")),
            alcohol=str(data.get("alcohol", "NO")),
            alcohol_frecuencia=str(data.get("alcohol_frecuencia", "")),
            drogas=str(data.get("drogas", "NO")),
            drogas_tipo=str(data.get("drogas_tipo", "")),
            coca=str(data.get("coca", "NO")),
            deporte=str(data.get("deporte", "NO")),
            deporte_detalle=str(data.get("deporte_detalle", "")),
            grupo_sanguineo=str(data.get("grupo_sanguineo", "")),
            historia_laboral=str(data.get("historia_laboral", "[]")),
            riesgos_expuestos=str(data.get("riesgos_expuestos", "[]")),
            observaciones=str(data.get("observaciones", "REGISTRO FINALIZADO"))
        )
        
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "Proceso Completo"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")

# --- RUTA 5: CONSULTA GENERAL ---
@app.get("/pacientes/")
def get_pacientes_list(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
