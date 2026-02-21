from fastapi import FastAPI, Depends, Request
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

@app.get("/")
def read_root():
    return {"proyecto": "HISTORIAL_CLINICO_NUBE", "estado": "online"}

@app.get("/api/paciente-completo/{id}")
def get_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p:
        return {"error": "Paciente no encontrado"}
    return {
        "paciente": {
            "nombre": p.nombre.upper(),
            "apellido": p.apellido.upper(),
            "ci": p.ci,
            "codigo_paciente": p.codigo_paciente.upper()
        },
        "datos": {k: v for k, v in p.__dict__.items() if not k.startswith('_')}
    }

@app.post("/p2/")
async def guardar_p2(r: Request, db: Session = Depends(get_db)):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    p = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if p:
        for k, v in data.items():
            if hasattr(p, k) and k != "paciente_id":
                setattr(p, k, str(v).upper())
        db.commit()
        return {"status": "ok"}
    return {"error": "no encontrado"}, 404

@app.post("/p3/")
async def guardar_p3(r: Request, db: Session = Depends(get_db)):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    p = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if p:
        for k, v in data.items():
            if hasattr(p, k) and k != "paciente_id":
                setattr(p, k, str(v).upper())
        db.commit()
        return {"status": "ok"}
    return {"error": "no encontrado"}, 404
