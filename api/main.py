import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# 1. INICIALIZACIÓN DE DB
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 2. CORS COMPLETO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. SESIÓN DE DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def check():
    return {"status": "online", "db": "connected"}

# --- RUTA 1: PACIENTES (EVITA DUPLICADOS DE CI) ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        ci_val = str(data.get("ci", ""))
        existente = db.query(models.Paciente).filter(models.Paciente.ci == ci_val).first()
        if existente:
            return existente
        db_obj = models.Paciente(
            nombre=str(data.get("nombre", "")),
            apellido=str(data.get("apellido", "")),
            ci=ci_val,
            codigo_paciente=str(data.get("codigo_paciente", ""))
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 2: FILIACIÓN (CORRECCIÓN DE ERROR 400 DEFINITIVA) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Validamos que el paciente_id exista, de lo contrario no podemos guardar la P1
        p_id = data.get("paciente_id")
        if not p_id:
            raise ValueError("Falta el ID del paciente en la solicitud")

        db_obj = models.DeclaracionJurada(
            paciente_id=int(p_id),
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
        # Esto nos dirá exactamente qué campo falla en los logs de Render
        raise HTTPException(status_code=400, detail=f"Error en validacion: {str(e)}")

# --- RUTA 3: P2 ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_obj = models.AntecedentesP2(**data)
        db.add(db_obj)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# --- RUTA 4: P3 ---
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

@app.get("/pacientes/")
def list_p(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
