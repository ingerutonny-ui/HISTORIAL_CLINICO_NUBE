from fastapi import FastAPI, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

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

def persistir_p2(data, p_id):
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
        print(f"Error DB: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "active"}

@app.get("/api/paciente-completo/{id}")
def get_p(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p: return {"error": "404"}
    return {
        "paciente": {
            "nombre": p.nombre, 
            "apellido": p.apellido, 
            "ci": p.ci, 
            "codigo": getattr(p, 'codigo_paciente', 'SIN CÓDIGO')
        }
    }

@app.post("/p2")
async def save_p2(r: Request, background_tasks: BackgroundTasks):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    background_tasks.add_task(persistir_p2, data, p_id)
    return {"status": "ok"}
