from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import json
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
    return crud.get_pacientes(db, skip, limit)

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
    db_habitos = crud.create_habitos(db=db, habitos=data)
    if not db_habitos:
        raise HTTPException(status_code=400, detail="Error al guardar")
    return {"status": "success"}

@app.get("/generar-pdf/{paciente_id}", response_class=HTMLResponse)
def generar_reporte_completo(paciente_id: int, db: Session = Depends(get_db)):
    data = crud.get_historial_completo(db, paciente_id)
    if not data["paciente"]:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    p, f, a, h = data["paciente"], data["filiacion"], data["antecedentes"], data["habitos"]

    filas_laboral = ""
    if h and h.historia_laboral:
        try:
            lista_lab = json.loads(h.historia_laboral)
            for it in lista_lab:
                filas_laboral += f"<tr><td>{it.get('edad','')}</td><td>{it.get('emp','')}</td><td>{it.get('ocu','')}</td><td>{it.get('tie','')}</td><td>{it.get('rie','')}</td><td>{it.get('epp','')}</td></tr>"
        except: pass
    
    while filas_laboral.count("<tr>") < 6:
        filas_laboral += "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 0; }}
            body {{ font-family: Arial, sans-serif; font-size: 8px; margin: 0; padding: 0; text-transform: uppercase; }}
            .page {{ width: 216mm; height: 279mm; padding: 15mm; box-sizing: border-box; page-break-after: always; }}
            .header {{ border: 1px solid #000; display: flex; text-align: center; }}
            .logo {{ width: 15%; border-right: 1px solid #000; padding: 5px; font-weight: bold; font-size: 14px; }}
            .title {{ width: 70%; padding: 5px; font-weight: bold; }}
            .section {{ background: #000; color: #fff; padding: 4px; font-weight: bold; margin-top: 10px; }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 2px; }}
            .table td {{ border: 1px solid #000; padding: 3px; }}
            .label {{ font-size: 6px; font-weight: bold; display: block; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header">
                <div class="logo">OHS</div>
                <div class="title">DECLARACIÓN JURADA DE SALUD</div>
                <div class="code">CÓDIGO: {p.codigo_paciente}</div>
            </div>
            <div class="section">1. AFILIACIÓN</div>
            <table class="table">
                <tr><td><span class="label">NOMBRE</span>{p.nombres} {p.apellidos}</td><td><span class="label">CI</span>{p.ci}</td></tr>
            </table>
            <div class="section">2. ANTECEDENTES</div>
            <table class="table">
                <tr><td>VISTA</td><td>{a.p1 if a else ''}</td><td>{a.d1 if a else ''}</td></tr>
                <tr><td>OSTEOMUSCULAR</td><td>{a.p10 if a else ''}</td><td>{a.d10 if a else ''}</td></tr>
            </table>
        </div>
        <div class="page">
            <div class="section">HISTORIA LABORAL</div>
            <table class="table">
                {filas_laboral}
            </table>
            <div class="section">3. HÁBITOS</div>
            <table class="table">
                <tr><td>ALCOHOL: {h.h2 if h else ''}</td><td>TABACO: {h.h1 if h else ''}</td><td>RIESGOS: {h.r6 if h else ''}</td></tr>
                <tr><td>GRUPO SANGUÍNEO: {h.r10 if h else ''}</td></tr>
            </table>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
