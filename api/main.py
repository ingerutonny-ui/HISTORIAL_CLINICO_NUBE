from fastapi import FastAPI, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# CORS configurado para evitar bloqueos de origen
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

# FUNCIÓN CRÍTICA: Guarda en disco sin bloquear la respuesta al usuario
def tarea_guardar_p2(data, p_id):
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
        print(f"Error asíncrono P2: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"proyecto": "HISTORIAL_CLINICO_NUBE", "status": "online"}

@app.get("/api/paciente-completo/{id}")
def get_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p: return {"error": "No encontrado"}
    p1 = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == id).first()
    
    return {
        "paciente": {
            "nombre": p.nombre, 
            "apellido": p.apellido, 
            "ci": p.ci,
            "codigo_paciente": getattr(p, 'codigo_paciente', "S/C")
        },
        "p1": {k: v for k, v in p1.__dict__.items() if not k.startswith('_')} if p1 else {},
        "p2": {k: v for k, v in p2.__dict__.items() if not k.startswith('_')} if p2 else {}
    }

@app.post("/p2")
async def guardar_p2(r: Request, background_tasks: BackgroundTasks):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    # Respondemos de inmediato para que el Frontend no de error de conexión
    background_tasks.add_task(tarea_guardar_p2, data, p_id)
    return {"status": "ok", "message": "Procesando en la nube"}
