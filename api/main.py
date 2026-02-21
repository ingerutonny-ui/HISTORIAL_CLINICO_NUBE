from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# CORS Ajustado para GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')

class Paciente(BaseModel):
    nombre: str; apellido: str; ci: str; codigo: Optional[str] = None

class Filiacion(BaseModel):
    paciente_id: int; edad: str; sexo: str; fecha_nacimiento: str; profesion_oficio: str

class P3Data(BaseModel):
    paciente_id: int
    grupo_sanguineo: str
    fuma: str
    alcohol: str
    drogas: str
    coca: str  # Sincronizado con la base de datos
    deporte: str
    historia_laboral: str 
    riesgos_expuestos: str
    observaciones: Optional[str] = "REGISTRO COMPLETADO"

@app.post("/api/pacientes")
async def crear_paciente(p: Paciente):
    conn = get_db_connection(); cur = conn.cursor()
    codigo_gen = f"{p.nombre[:1]}{p.apellido[:1]}{p.ci[-4:]}".upper()
    try:
        cur.execute("INSERT INTO pacientes (nombre, apellido, ci, codigo) VALUES (%s, %s, %s, %s) RETURNING id", (p.nombre, p.apellido, p.ci, codigo_gen))
        p_id = cur.fetchone()[0]
        conn.commit()
        return {"id": p_id, "codigo": codigo_gen}
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()

@app.post("/api/p3/")
async def guardar_p3(d: P3Data):
    conn = get_db_connection(); cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO p3 (paciente_id, grupo_sanguineo, fuma, alcohol, drogas, coca, deporte, 
            historia_laboral, riesgos_expuestos, observaciones) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (d.paciente_id, d.grupo_sanguineo, d.fuma, d.alcohol, d.drogas, d.coca, d.deporte,
             d.historia_laboral, d.riesgos_expuestos, d.observaciones))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close(); conn.close()

@app.get("/api/paciente-completo/{p_id}")
async def obtener_todo(p_id: int):
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM pacientes WHERE id = %s", (p_id,))
        paciente = cur.fetchone()
        cur.execute("SELECT * FROM filiacion WHERE paciente_id = %s", (p_id,))
        filiacion = cur.fetchone()
        cur.execute("SELECT * FROM p2 WHERE paciente_id = %s", (p_id,))
        p2 = cur.fetchone()
        cur.execute("SELECT * FROM p3 WHERE paciente_id = %s", (p_id,))
        p3 = cur.fetchone()
        return {"paciente": paciente, "filiacion": filiacion, "p2": p2, "p3": p3}
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
