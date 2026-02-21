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

# Modelo de datos P3 ajustado a los IDs del Frontend
class P3Data(BaseModel):
    paciente_id: int
    fuma: str
    alcohol: str
    drogas: str
    coca: str  # Mapeado desde el campo 'pijchar' del frontend
    deporte: str
    grupo_sanguineo: str
    historia_laboral: str  # JSON string
    riesgos_expuestos: str # JSON string
    observaciones: Optional[str] = "REGISTRO COMPLETADO"

# Base de datos temporal (Esto debe conectar a tu PostgreSQL luego)
db_p3 = []

@app.post("/api/guardar-p3")
async def guardar_p3(data: P3Data):
    try:
        # En el futuro, aquí va: insert_en_postgres(data.dict())
        db_p3.append(data.dict())
        print(f"Datos recibidos para paciente {data.paciente_id}")
        return {"status": "success", "message": "P3 Sincronizado correctamente"}
    except Exception as e:
        print(f"Error en backend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/paciente-completo/{p_id}")
async def get_paciente_completo(p_id: int):
    # Simulación de retorno de datos para la barra superior
    return {
        "paciente": {
            "nombre": "PACIENTE", 
            "apellido": "IDENTIFICADO", 
            "ci": "1234567",
            "codigo": f"PX-{p_id}"
        }
    }
