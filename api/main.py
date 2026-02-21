from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Importaciones relativas según tu estructura de carpetas
try:
    from . import models, schemas, crud
    from .database import SessionLocal, engine
except ImportError:
    import models, schemas, crud
    from database import SessionLocal, engine

# Crear tablas en PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS para GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de la Base de Datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTA PARA GUARDAR P3
@app.post("/api/guardar-p3")
async def guardar_p3(data: schemas.HabitosRiesgosP3Base, db: Session = Depends(get_db)):
    try:
        # Usamos la función upsert_p3 de tu archivo crud.py
        resultado = crud.upsert_p3(db, data.dict())
        return {"status": "success", "message": "P3 Guardado en PostgreSQL", "id": resultado.id}
    except Exception as e:
        print(f"Error en Guardar P3: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# RUTA PARA CARGAR DATOS DEL PACIENTE EN LA BARRA SUPERIOR
@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == p_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
