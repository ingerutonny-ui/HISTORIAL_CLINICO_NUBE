import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# 1. INICIALIZACIÓN DE DB
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE", version="2.5.0")

# 2. CORS TOTAL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. SESIÓN DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "online", "database": str(database.SQLALCHEMY_DATABASE_URL)}

# --- RUTA 1: REGISTRO PACIENTES (P0) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        ci_recibido = str(data.get("ci", ""))
        
        # Si el paciente ya existe por CI, lo devolvemos para evitar el error 'Unique'
        existente = db.query(models.Paciente).filter(models.Paciente.ci == ci_recibido).first()
        if existente:
            return existente
            
        db_obj = models.Paciente(
            nombre=str(data.get("nombre", "")),
            apellido=str(data.get("apellido", "")),
            ci=ci_recibido,
            codigo_paciente=str(data.get("codigo_paciente", ""))
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en P0: {str(e)}")

# --- RUTA 2: PARTE 1 - FILIACIÓN (SOLUCIÓN ERROR 400) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # FORZAMOS TODO A STRING para que coincida con models.py y SQLite
        # El error 400 ocurre porque el HTML envía 'edad' como Integer
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
        return {"status": "success", "detail": "P1 Guardada"}
    except Exception as e:
        db.rollback()
        print(f"DEBUG ERROR P1: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 3: PARTE 2 - ANTECEDENTES (22 CAMPOS) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Limpiamos los datos para asegurar que todos sean Strings antes de guardar
        campos_p2 = {k: str(v) if k != 'paciente_id' else v for k, v in data.items()}
        
        db_obj = models.AntecedentesP2(**campos_p2)
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 4: PARTE 3 - HÁBITOS Y RIESGOS ---
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
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
