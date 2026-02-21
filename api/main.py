from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import schemas, crud, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/guardar-p3")
async def guardar_p3(data: schemas.P3Data, db: Session = Depends(get_db)):
    try:
        # Llamamos a la función de guardado real en tu archivo crud.py
        exito = crud.crear_p3(db, data)
        if exito:
            return {"status": "success", "message": "P3 Guardado en PostgreSQL"}
        raise HTTPException(status_code=400, detail="No se pudo guardar en la DB")
    except Exception as e:
        print(f"Error Crítico: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int, db: Session = Depends(get_db)):
    paciente = crud.obtener_paciente_por_id(db, p_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": paciente}
