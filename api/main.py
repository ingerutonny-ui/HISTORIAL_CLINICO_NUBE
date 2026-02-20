from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

app = FastAPI()

# Configuración CORS robusta
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
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

@app.get("/api/paciente-completo/{paciente_id}")
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    # Buscamos en declaraciones_p1 (según tu models.py)
    filiacion = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == paciente_id).first()
    
    return {
        "paciente": paciente,
        "filiacion": filiacion if filiacion else {}
    }

@app.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db)):
    if crud.delete_paciente(db, paciente_id):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Error al eliminar")
