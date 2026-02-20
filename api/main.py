from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Intento de sincronización forzada al arrancar
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("Base de datos sincronizada exitosamente")
except Exception as e:
    print(f"Error de sincronización: {e}")

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

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en consulta de pacientes")

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

@app.post("/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

@app.post("/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)

@app.post("/enfermeras/")
async def save_enfermera(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_enfermera(db, data)

@app.post("/doctores/")
async def save_doctor(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_doctor(db, data)

@app.get("/api/paciente-completo/{paciente_id}")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {
        "paciente": paciente,
        "filiacion": db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first() or {},
        "p2": db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == paciente_id).first() or {},
        "p3": db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == paciente_id).first() or {}
    }

@app.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db)):
    if crud.delete_paciente(db, paciente_id):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="No se pudo eliminar")
