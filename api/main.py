from fastapi import FastAPI, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# Configuración CORS robusta para evitar bloqueos en Render
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

# Función de procesado en segundo plano para evitar Timeouts
def procesar_guardado_p2(data, p_id):
    db = database.SessionLocal()
    try:
        obj = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == p_id).first()
        if not obj:
            obj = models.AntecedentesP2(paciente_id=p_id)
            db.add(obj)
            
        for k, v in data.items():
            if hasattr(obj, k) and k != "paciente_id":
                setattr(obj, k, str(v).upper())
        db.commit()
    except Exception as e:
        print(f"Error en segundo plano: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"proyecto": "HISTORIAL_CLINICO_NUBE", "estado": "online"}

@app.get("/api/paciente-completo/{id}")
def get_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p: return {"error": "No encontrado"}
    p1 = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == id).first()
    
    return {
        "paciente": {
            "nombre": p.nombre, 
            "apellido": p.apellido, 
            "ci": p.ci,
            "codigo_paciente": getattr(p, 'codigo_paciente', "S/C")
        },
        "p1": {k: v for k, v in p1.__dict__.items() if not k.startswith('_')} if p1 else {},
        "p2": {k: v for k, v in p2.__dict__.items() if not k.startswith('_')} if p2 else {},
        "p3": {k: v for k, v in p3.__dict__.items() if not k.startswith('_')} if p3 else {}
    }

@app.post("/p2")
async def guardar_p2(r: Request, background_tasks: BackgroundTasks):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    # Respondemos de inmediato y guardamos después
    background_tasks.add_task(procesar_guardado_p2, data, p_id)
    return {"status": "ok", "message": "Procesando en segundo plano"}

@app.post("/p3")
async def guardar_p3(r: Request, db: Session = Depends(get_db)):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    obj = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == p_id).first()
    if not obj:
        obj = models.HabitosRiesgosP3(paciente_id=p_id)
        db.add(obj)
    for k, v in data.items():
        if hasattr(obj, k) and k != "paciente_id":
            val = ", ".join(v) if isinstance(v, list) else str(v)
            setattr(obj, k, val.upper())
    db.commit()
    return {"status": "ok"}
