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

@app.get("/api/paciente-completo/{id}")
def get_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p: return {"error": "No existe"}
    
    # Buscamos en las otras tablas para el reporte
    p1 = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == id).first()
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == id).first()
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == id).first()
    
    return {
        "paciente": {"nombre": p.nombre, "apellido": p.apellido, "ci": p.ci, "codigo": p.codigo_paciente},
        "p1": {k: v for k, v in p1.__dict__.items() if not k.startswith('_')} if p1 else {},
        "p2": {k: v for k, v in p2.__dict__.items() if not k.startswith('_')} if p2 else {},
        "p3": {k: v for k, v in p3.__dict__.items() if not k.startswith('_')} if p3 else {}
    }

@app.post("/p2/")
async def guardar_p2(r: Request, db: Session = Depends(get_db)):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    # Buscamos si ya existe el registro en AntecedentesP2
    p2 = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == p_id).first()
    if not p2:
        p2 = models.AntecedentesP2(paciente_id=p_id)
        db.add(p2)
    
    # Mapeo dinámico solo para la tabla AntecedentesP2
    for k, v in data.items():
        if hasattr(p2, k) and k != "paciente_id":
            setattr(p2, k, str(v).upper())
    
    db.commit()
    return {"status": "ok"}

@app.post("/p3/")
async def guardar_p3(r: Request, db: Session = Depends(get_db)):
    data = await r.json()
    p_id = int(data.get("paciente_id"))
    # Buscamos si ya existe en HabitosRiesgosP3
    p3 = db.query(models.HabitosRiesgosP3).filter(models.HabitosRiesgosP3.paciente_id == p_id).first()
    if not p3:
        p3 = models.HabitosRiesgosP3(paciente_id=p_id)
        db.add(p3)
    
    for k, v in data.items():
        if hasattr(p3, k) and k != "paciente_id":
            setattr(p3, k, str(v).upper())
            
    db.commit()
    return {"status": "ok"}
