from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Solo crea tablas si NO existen.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración de CORS con máxima apertura para evitar bloqueos en GitHub Pages
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

# RUTA DEL REPORTE: Optimizada para evitar el Error 500 y problemas de CORS
@app.get("/pacientes/{paciente_id}")
def get_paciente_reporte(paciente_id: int, db: Session = Depends(get_db)):
    # 1. Buscamos datos básicos (Si esto falla, el ID no existe)
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # 2. Buscamos filiación con manejo de error total
    filiacion_data = {}
    try:
        f = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
        if f:
            filiacion_data = {
                "sexo": f.sexo, "edad": f.edad, "estado_civil": f.estado_civil,
                "lugar_nacimiento": f.lugar_nacimiento, "domicilio": f.domicilio,
                "n_casa": f.n_casa, "zona_barrio": f.zona_barrio, "ciudad": f.ciudad,
                "pais": f.pais, "telefono": f.telefono, "profesion_oficio": f.profesion_oficio
            }
    except Exception:
        pass # Si falla la tabla P1, seguimos adelante con datos básicos

    # 3. Respuesta unificada (Garantiza que el JSON tenga todos los campos que espera el HTML)
    return {
        "id": paciente.id,
        "codigo_paciente": paciente.codigo_paciente or "---",
        "nombre": paciente.nombre or "",
        "apellido": paciente.apellido or "",
        "ci": paciente.ci or "---",
        "fecha_nacimiento": paciente.fecha_nacimiento or "---",
        "sexo": filiacion_data.get("sexo") or "---",
        "edad": filiacion_data.get("edad") or "---",
        "estado_civil": filiacion_data.get("estado_civil") or "---",
        "lugar_nacimiento": filiacion_data.get("lugar_nacimiento") or "---",
        "domicilio": filiacion_data.get("domicilio") or "---",
        "n_casa": filiacion_data.get("n_casa") or "---",
        "zona_barrio": filiacion_data.get("zona_barrio") or "---",
        "ciudad": filiacion_data.get("ciudad") or "---",
        "pais": filiacion_data.get("pais") or "---",
        "telefono": filiacion_data.get("telefono") or "---",
        "profesion_oficio": filiacion_data.get("profesion_oficio") or "---"
    }

# --- RUTAS DE SECCIONES ---

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.upsert_filiacion(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p2(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p3(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
