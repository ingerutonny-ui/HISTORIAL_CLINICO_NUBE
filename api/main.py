from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Solo crea tablas si NO existen.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS DE PACIENTES ---

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# RUTA UNIFICADA: Cruza datos de Paciente y Filiación (P1) para el reporte
@app.get("/pacientes/{paciente_id}")
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    # 1. Buscar datos básicos del paciente
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # 2. Buscar datos de la Sección P1 (Filiación)
    filiacion = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
    
    # 3. Construir respuesta unificada para mapear todos los campos del reporte
    return {
        "id": paciente.id,
        "codigo_paciente": paciente.codigo_paciente,
        "nombre": paciente.nombre,
        "apellido": paciente.apellido,
        "ci": paciente.ci,
        "fecha_nacimiento": paciente.fecha_nacimiento,
        # Datos desde Filiacion (si no existen, devuelve "---")
        "sexo": filiacion.sexo if filiacion else "---",
        "edad": filiacion.edad if filiacion else "---",
        "estado_civil": filiacion.estado_civil if filiacion else "---",
        "lugar_nacimiento": filiacion.lugar_nacimiento if filiacion else "---",
        "domicilio": filiacion.domicilio if filiacion else "---",
        "n_casa": filiacion.n_casa if filiacion else "---",
        "zona_barrio": filiacion.zona_barrio if filiacion else "---",
        "ciudad": filiacion.ciudad if filiacion else "---",
        "pais": filiacion.pais if filiacion else "---",
        "telefono": filiacion.telefono if filiacion else "---",
        "profesion_oficio": filiacion.profesion_oficio if filiacion else "---"
    }

# --- RUTAS DE SECCIONES (P1, P2, P3) ---

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.upsert_filiacion(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p2(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p3(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")
