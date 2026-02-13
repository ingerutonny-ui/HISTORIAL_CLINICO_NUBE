from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Solo crea tablas si NO existen en la base de datos de Render
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración de CORS para que tu Frontend en GitHub Pages hable con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

# --- LECTURA PARA CRUD Y REPORTES OFICIALES ---
@app.get("/api/paciente-completo/{paciente_id}")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    # Buscamos al paciente base
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado en la nube")
    
    # Mapeo exacto basado en tu models.py para evitar errores de carga
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first()

    return {
        "paciente": paciente,
        "filiacion": filiacion if filiacion else {},
        "p2": p2 if p2 else {},
        "p3": p3 if p3 else {}
    }

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    # Lista todos los registros para tu lista_historial.html
    return db.query(models.Paciente).all()

# --- ESCRITURA Y GUARDADO ---
@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
    # Verificamos si ya existe por CI para evitar duplicados
    paciente = crud.get_paciente_by_ci(db, ci)
    if not paciente:
        paciente = crud.create_paciente(db, data)
    return paciente

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.upsert_filiacion(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Parte 1: {str(e)}")

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p2(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Parte 2: {str(e)}")

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p3(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Parte 3: {str(e)}")

# --- ACCIÓN DE ELIMINACIÓN DEFINITIVA ---
@app.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db)):
    # Llama a la función del crud.py que ya corregimos
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inge, el registro no existe o ya fue borrado.")
    return {"status": "success", "message": "Registro eliminado correctamente"}
