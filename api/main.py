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
    
    p, f, a, h = data["paciente"], data["filiacion"], data["antecedentes"], data["habitos"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 0; }}
            body {{ font-family: Arial, sans-serif; font-size: 9px; margin: 0; padding: 0; }}
            .page {{ width: 216mm; height: 279mm; padding: 15mm; box-sizing: border-box; page-break-after: always; position: relative; }}
            .header-box {{ border: 1px solid #000; display: flex; align-items: center; text-align: center; margin-bottom: 10px; }}
            .logo-area {{ width: 20%; font-weight: bold; font-size: 20px; border-right: 1px solid #000; padding: 10px; }}
            .title-area {{ width: 60%; padding: 5px; }}
            .code-area {{ width: 20%; border-left: 1px solid #000; padding: 5px; }}
            
            .section-title {{ background: #000; color: #fff; padding: 4px; font-weight: bold; text-transform: uppercase; margin-top: 10px; border: 1px solid #000; }}
            .grid-table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
            .grid-table td {{ border: 1px solid #000; padding: 4px; vertical-align: top; }}
            .label {{ font-size: 7px; font-weight: bold; display: block; text-transform: uppercase; }}
            
            .med-row {{ display: flex; border: 1px solid #000; border-top: none; align-items: stretch; }}
            .med-label {{ width: 25%; font-weight: bold; border-right: 1px solid #000; padding: 3px; display: flex; align-items: center; }}
            .med-val {{ width: 10%; border-right: 1px solid #000; padding: 3px; text-align: center; font-weight: bold; }}
            .med-desc {{ width: 65%; padding: 3px; font-size: 8px; }}
            
            .footer-legal {{ margin-top: 20px; text-align: justify; border: 1px solid #000; padding: 10px; line-height: 1.4; }}
            .signature-box {{ margin-top: 40px; text-align: center; }}
            .line {{ border-top: 1px solid #000; width: 250px; margin: 0 auto; padding-top: 5px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header-box">
                <div class="logo-area">ohs</div>
                <div class="title-area">
                    <b style="font-size: 14px;">DECLARACIÓN JURADA DE SALUD</b><br>
                    <span>TRABAJO SANO, SEGURO Y PRODUCTIVO</span>
                </div>
                <div class="code-area">
                    <span class="label">CÓDIGO</span>
                    <b>{p.codigo_paciente}</b>
                </div>
            </div>

            <div class="section-title">1. AFILIACIÓN DEL TRABAJADOR</div>
            <table class="grid-table">
                <tr>
                    <td colspan="3"><span class="label">Apellidos y Nombres</span><b>{p.nombres} {p.apellidos}</b></td>
                    <td><span class="label">Edad</span>{f.edad if f else ''} AÑOS</td>
                    <td><span class="label">Sexo</span>{f.sexo if f else ''}</td>
                </tr>
                <tr>
                    <td><span class="label">Fecha Nacimiento</span>{f.fecha_nacimiento if f else ''}</td>
                    <td><span class="label">C.I.</span>{p.ci}</td>
                    <td colspan="3"><span class="label">Domicilio</span>{f.domicilio if f else ''} #{f.n_casa if f else ''} - {f.ciudad if f else ''}</td>
                </tr>
            </table>

            <div class="section-title">2. ANTECEDENTES PATOLÓGICOS</div>
            <div style="border-top: 1px solid #000;">
                <div class="med-row">
                    <div class="med-label">VISTA</div><div class="med-val">{a.p1 if a else ''}</div>
                    <div class="med-desc">Glaucoma, Miopía, Daltonismo, Pterigión: {a.d1 if a else ''}</div>
                </div>
                <div class="med-row">
                    <div class="med-label">AUDITIVO</div><div class="med-val">{a.p2 if a else ''}</div>
                    <div class="med-desc">Hipoacusia, Vértigo, Otitis: {a.d2 if a else ''}</div>
                </div>
                <div class="med-row">
                    <div class="med-label">RESPIRATORIOS</div><div class="med-val">{a.p3 if a else ''}</div>
                    <div class="med-desc">TBC, Asma, Bronquitis, Rinitis: {a.d3 if a else ''}</div>
                </div>
                <div class="med-row">
                    <div class="med-label">CARDIOVASCULARES</div><div class="med-val">{a.p4 if a else ''}</div>
                    <div class="med-desc">Hipertensión, Soplos, Infartos: {a.d4 if a else ''}</div>
                </div>
                <div class="med-row">
                    <div class="med-label">DIGESTIVOS</div><div class="med-val">{a.p5 if a else ''}</div>
                    <div class="med-desc">Gastritis, Úlceras, Hemorroides: {a.d5 if a else ''}</div>
                </div>
                </div>
        </div>

        <div class="page">
            <div class="section-title">ANTECEDENTES OCUPACIONALES (HISTORIA LABORAL)</div>
            <table class="grid-table">
                <tr style="background: #eee; font-weight: bold; text-align: center;">
                    <td>Edad Inicio</td><td>Empresa</td><td>Ocupación</td><td>Tiempo</td><td>Riesgos</td><td>EPP</td>
                </tr>
                {"".join([f"<tr><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>" for _ in range(5)])}
            </table>

            <div class="section-title">3. HÁBITOS</div>
            <table class="grid-table">
                <tr>
                    <td><b>ALCOHOL:</b> {h.h2 if h else ''} ({h.r2 if h else ''})</td>
                    <td><b>TABACO:</b> {h.h1 if h else ''} ({h.r1 if h else ''})</td>
                </tr>
                <tr>
                    <td><b>PIJCHAR/BOLO:</b> {h.h4 if h else ''}</td>
                    <td><b>GRUPO SANGUÍNEO:</b> {h.r10 if h else ''}</td>
                </tr>
            </table>

            <div class="footer-legal">
                Por medio de este documento médico legal declaro que es verdad toda la información proporcionada. Cualquier omisión o falsedad invalida el presente de acuerdo a normativa del Ministerio de Salud.
            </div>

            <div class="signature-box">
                <div class="line">FIRMA DEL TRABAJADOR / PACIENTE</div>
                C.I. {p.ci}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
