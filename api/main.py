from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

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

@app.post("/pacientes/")
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.get("/pacientes/")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/filiacion/")
def save_p1(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.DeclaracionJurada(**data.dict())
        db.add(new_entry)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p2/")
def save_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.AntecedentesP2(**data.dict())
        db.add(new_entry)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
