from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

# Sincronización estructural: Borra tablas viejas y crea las nuevas con todas las columnas
models.Base.metadata.drop_all(bind=database.engine)
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

@app.get("/")
def health_check():
    return {"status": "online", "project": "HISTORIAL_CLINICO_NUBE"}

@app.post("/pacientes/")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ci = str(data.get("ci"))
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
        raise HTTPException(status_code=400, detail=f"Error en P1: {str(e)}")

@app.post("/declaraciones/p2/")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p2(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P2: {str(e)}")

@app.post("/declaraciones/p3/")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        return crud.create_p3(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en P3: {str(e)}")

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
