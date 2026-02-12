from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Inicialización de DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CONFIGURACIÓN DE CORS DEFINITIVA
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ingerutonny-ui.github.io",
        "http://localhost:3000",
        "*"
    ],
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

# RUTA ÚNICA PARA EL REPORTE (CRUD READ)
@app.get("/api/reporte-unificado/{paciente_id}")
def get_reporte_unificado(paciente_id: int, db: Session = Depends(get_db)):
    try:
        paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        filiacion = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente_id).first()
        p2 = db.query(models.DeclaracionP2).filter(models.DeclaracionP2.paciente_id == paciente_id).first()
        p3 = db.query(models.DeclaracionP3).filter(models.DeclaracionP3.paciente_id == paciente_id).first()

        return {
            "paciente": paciente,
            "filiacion": filiacion if filiacion else {},
            "p2": p2 if p2 else {},
            "p3": p3 if p3 else {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RESTO DEL CRUD
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
