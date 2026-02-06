from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pacientes(db, skip=skip, limit=limit)

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.post("/filiacion/")
def save_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/declaraciones/p2/")
def save_p2(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/declaraciones/p3/")
def save_p3(data: schemas.HabitosCreate, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=data)

@app.get("/generar-pdf/{paciente_id}", response_class=HTMLResponse)
def generar_reporte_completo(paciente_id: int, db: Session = Depends(get_db)):
    data = crud.get_historial_completo(db, paciente_id)
    if not data["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p = data["paciente"]
    f = data["filiacion"]
    a = data["antecedentes"]
    h = data["habitos"]

    html_content = f"""
    <html>
        <head>
            <title>Historial Clínico - {p.nombres}</title>
            <style>
                body {{ font-family: sans-serif; padding: 40px; color: #333; }}
                .header {{ text-align: center; border-bottom: 2px solid #24a174; padding-bottom: 10px; }}
                h1 {{ color: #24a174; margin-bottom: 5px; }}
                .section {{ margin-top: 25px; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
                .section-title {{ font-weight: bold; background: #f4f4f4; padding: 5px; display: block; margin-bottom: 10px; text-transform: uppercase; }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
                .label {{ font-weight: bold; font-size: 0.8em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>HISTORIAL CLÍNICO DIGITAL</h1>
                <p>CÓDIGO PACIENTE: <strong>{p.codigo_paciente}</strong></p>
            </div>
            
            <div class="section">
                <span class="section-title">1. Datos Personales (Filiación)</span>
                <div class="grid">
                    <div><span class="label">NOMBRES:</span> {p.nombres} {p.apellidos}</div>
                    <div><span class="label">CI:</span> {p.ci}</div>
                    <div><span class="label">EDAD:</span> {f.edad if f else 'S/D'} años</div>
                    <div><span class="label">SEXO:</span> {f.sexo if f else 'S/D'}</div>
                    <div><span class="label">CIUDAD:</span> {f.ciudad if f else 'S/D'}</div>
                </div>
            </div>

            <div class="section">
                <span class="section-title">2. Antecedentes Patológicos</span>
                <p>¿Diabetes?: {a.p1 if a else 'S/D'} | ¿Hipertensión?: {a.p2 if a else 'S/D'}</p>
                <p>¿Alergias?: {a.p11 if a else 'S/D'} | Detalle: {a.d11 if a else 'S/D'}</p>
            </div>

            <div class="section">
                <span class="section-title">3. Hábitos y Riesgos</span>
                <p>¿Fuma?: {h.h1 if h else 'S/D'} | ¿Bebe?: {h.h2 if h else 'S/D'}</p>
                <p>Grupo Sanguíneo: {h.r10 if h else 'S/D'}</p>
            </div>

            <div style="margin-top: 50px; text-align: center; font-size: 0.7em; color: #aaa;">
                Documento generado automáticamente por HISTORIAL_CLINICO_NUBE
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
