from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

# Inicialización de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración estricta de CORS para eliminar el error de tu consola
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        return Response(status_code=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        })
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Dependency para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTA DE CONSULTA INTEGRAL ---
@app.get("/api/paciente-completo/{identificador}")
def obtener_paciente_completo(identificador: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.codigo_paciente == identificador).first()
    if not paciente and identificador.isdigit():
        paciente = db.query(models.Paciente).filter(models.Paciente.id == int(identificador)).first()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    filiacion = db.query(models.Filiacion).filter(models.Filiacion.paciente_id == paciente.id).first()
    return {"paciente": paciente, "filiacion": filiacion}

# --- RUTAS DE REGISTRO Y GESTIÓN DE DATOS ---
@app.post("/pacientes/")
def registrar_paciente(data: dict, db: Session = Depends(get_db)):
    return crud.create_paciente(db, data)

@app.post("/filiacion/")
def registrar_filiacion(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_filiacion(db, data)

@app.post("/antecedentes_p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p2(db, data)

@app.post("/habitos_p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)):
    return crud.upsert_p3(db, data)

# --- GESTIÓN DE PERSONAL ---
@app.get("/personal/")
def obtener_personal(db: Session = Depends(get_db)):
    return {
        "doctores": db.query(models.Doctor).all(),
        "enfermeras": db.query(models.Enfermera).all()
    }

@app.post("/doctores/")
def registrar_doctor(data: dict, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data)

@app.put("/doctores/{id_doc}")
def actualizar_doctor(id_doc: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.items(): setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.delete("/doctores/{id_doc}")
def borrar_doctor(id_doc: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id_doc == id_doc).first()
    if not doctor: raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Eliminado"}

@app.post("/enfermeras/")
def registrar_enfermera(data: dict, db: Session = Depends(get_db)):
    return crud.create_enfermera(db, data)

@app.put("/enfermeras/{id_enfe}")
def actualizar_enfermera(id_enfe: int, data: dict, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    for key, value in data.items(): setattr(enfermera, key, value)
    db.commit()
    db.refresh(enfermera)
    return enfermera

@app.delete("/enfermeras/{id_enfe}")
def borrar_enfermera(id_enfe: int, db: Session = Depends(get_db)):
    enfermera = db.query(models.Enfermera).filter(models.Enfermera.id_enfe == id_enfe).first()
    if not enfermera: raise HTTPException(status_code=404, detail="No encontrada")
    db.delete(enfermera)
    db.commit()
    return {"message": "Eliminada"}
