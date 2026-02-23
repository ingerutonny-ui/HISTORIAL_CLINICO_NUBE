from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud

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

# --- SECCIÓN PERSONAL (RUTAS DINÁMICAS SIN ERROR DE BARRA) ---
@app.post("/doctor", status_code=status.HTTP_201_CREATED)
@app.post("/doctor/", status_code=status.HTTP_201_CREATED)
async def save_doctor(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        nuevo_doc = crud.create_doctor(db, data)
        if not nuevo_doc:
            raise HTTPException(status_code=400, detail="No se pudo crear el registro")
        return nuevo_doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctores")
@app.get("/doctores/")
def list_doctores(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

@app.post("/enfermera", status_code=status.HTTP_201_CREATED)
@app.post("/enfermera/", status_code=status.HTTP_201_CREATED)
async def save_enfermera(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        nueva_enf = crud.create_enfermera(db, data)
        if not nueva_enf:
            raise HTTPException(status_code=400, detail="No se pudo crear el registro")
        return nueva_enf
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/enfermeras")
@app.get("/enfermeras/")
def list_enfermeras(db: Session = Depends(get_db)):
    return db.query(models.Enfermera).all()

# --- SECCIÓN PACIENTES E INTEGRIDAD (MANTENIDA) ---
@app.get("/pacientes")
def list_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes")
async def save_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.create_paciente(db, data)

@app.post("/filiacion")
async def save_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_filiacion(db, data)

@app.post("/p2")
async def save_p2(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p2(db, data)

@app.post("/p3")
async def save_p3(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return crud.upsert_p3(db, data)
