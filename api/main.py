from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

# CONFIGURACIÓN CORS: Vital para que GitHub Pages hable con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos P3 con todos los campos de la Sección III
class P3Data(BaseModel):
    paciente_id: int
    fuma: str
    alcohol: str
    drogas: str
    coca: str
    deporte: str
    grupo_sanguineo: str
    historia_laboral: str  # JSON string
    riesgos_expuestos: str # JSON string (AQUÍ VAN LOS 12 RIESGOS)
    observaciones: Optional[str] = "REGISTRO COMPLETADO"

# Base de datos temporal (Simulada para el ejemplo, usa tu lógica de DB aquí)
db_p3 = []

@app.post("/api/guardar-p3")
async def guardar_p3(data: P3Data):
    try:
        # Aquí guardas en tu base de datos PostgreSQL
        db_p3.append(data.dict())
        return {"status": "success", "message": "P3 Sincronizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int):
    # Lógica para devolver P1, P2 y P3 juntos
    return {"paciente": {"nombre": "RUBEN", "apellido": "ALMENDRAS", "codigo": "RA6678"}}
