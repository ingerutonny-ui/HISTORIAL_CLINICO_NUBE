from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# Forzar creación de tablas en el DISK
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración de CORS total para evitar bloqueos
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
def root():
    return {"status": "ok", "storage": "DISK", "project": "HISTORIAL_CLINICO_NUBE"}

@app.get("/pacientes/")
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        db_paciente = models.Paciente(**data)
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        # Filtramos campos que no pertenezcan al modelo para evitar el Error 500
        allowed_fields = [c.key for c in models.DeclaracionJurada.__table__.columns]
        filtered_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        db_filiacion = models.DeclaracionJurada(**filtered_data)
        db.add(db_filiacion)
        db.commit()
        db.refresh(db_filiacion)
        return {"status": "success", "message": "Datos guardados en DISK"}
    except Exception as e:
        db.rollback()
        # Enviamos el error real para capturarlo si falla
        return {"status": "error", "detail": str(e)}
