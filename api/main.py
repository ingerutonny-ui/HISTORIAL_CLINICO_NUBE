from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

models.Base.metadata.create_all(bind=database.engine)

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

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# RUTA MAESTRA PARA EL REPORTE (CRUD READ)
@app.get("/reporte/{paciente_id}")
def get_full_report(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="No existe")
    
    # Intentamos obtener datos de todas las secciones, si no hay, devolvemos objeto vacío
    def get_data(model):
        try:
            res = db.query(model).filter(model.paciente_id == paciente_id).first()
            return res if res else {}
        except:
            return {}

    return {
        "p": paciente,
        "f1": get_data(models.Filiacion),
        "p2": get_data(models.DeclaracionP2),
        "p3": get_data(models.DeclaracionP3)
    }

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)
