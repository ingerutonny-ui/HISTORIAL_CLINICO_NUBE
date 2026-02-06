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
    db_habitos = crud.create_habitos(db=db, habitos=data)
    if not db_habitos:
        raise HTTPException(status_code=400, detail="Error al finalizar el registro")
    return {"status": "success", "message": "Registro completado exitosamente"}

@app.get("/generar-pdf/{paciente_id}", response_class=HTMLResponse)
def generar_reporte_completo(paciente_id: int, db: Session = Depends(get_db)):
    data = crud.get_historial_completo(db, paciente_id)
    if not data["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p, f, a, h = data["paciente"], data["filiacion"], data["antecedentes"], data["habitos"]

    filas_laboral = ""
    if h and h.historia_laboral:
        try:
            lista_lab = json.loads(h.historia_laboral)
            for it in lista_lab:
                filas_laboral += f"<tr><td>{it.get('edad','')}</td><td>{it.get('emp','')}</td><td>{it.get('ocu','')}</td><td>{it.get('tie','')}</td><td>{it.get('rie','')}</td><td>{it.get('epp','')}</td></tr>"
        except:
            pass
    
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
            .logo {{ width: 20%; border-right: 1px solid #000; padding: 5px; font-weight: bold; font-size: 14px; }}
            .title {{ width: 60%; padding: 5px; font-weight: bold; }}
            .code {{ width: 20%; border-left: 1px solid #000; padding: 5px; }}
            .section {{ background: #000; color: #fff; padding: 4px; font-weight: bold; margin-top: 10px; border: 1px solid #000; }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 2px; }}
            .table td {{ border: 1px solid #000; padding: 3px; }}
            .label {{ font-size: 6px; font-weight: bold; display: block; }}
            .sig {{ margin-top: 40px; text-align: center; }}
            .line {{ border-top: 1px solid #000; width: 250px; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header">
                [cite_start]<div class="logo">ohs [cite: 1]</div>
                [cite_start]<div class="title">DECLARACION JURADA DE SALUD [cite: 2][cite_start]<br>TRABAJO SANO, SEGURO Y PRODUCTIVO [cite: 3]</div>
                <div class="code"><span class="label">CÓDIGO</span>{p.codigo_paciente}</div>
            </div>
            <div class="section">1. [cite_start]AFILIACION DEL TRABAJADOR [cite: 5]</div>
            <table class="table">
                [cite_start]<tr><td colspan="2"><span class="label">APELLIDOS Y NOMBRES [cite: 6][cite_start]</span>{p.nombres} {p.apellidos}</td><td><span class="label">EDAD [cite: 6][cite_start]</span>{f.edad if f else ''}</td><td><span class="label">SEXO [cite: 7]</span>{f.sexo if f else ''}</td></tr>
                [cite_start]<tr><td><span class="label">CI [cite: 15][cite_start]</span>{p.ci}</td><td><span class="label">FECHA NAC. [cite: 10][cite_start]</span>{f.fecha_nacimiento if f else ''}</td><td colspan="2"><span class="label">DOMICILIO [cite: 15]</span>{f.domicilio if f else ''}</td></tr>
            </table>
            <div class="section">2. [cite_start]ANTECEDENTES PATOLÓGICOS [cite: 24]</div>
            <table class="table">
                [cite_start]<tr style="background:#eee"><td>SISTEMA</td><td>SI/NO [cite: 34, 35][cite_start]</td><td>DETALLES [cite: 36]</td></tr>
                [cite_start]<tr><td>VISTA [cite: 25]</td><td>{a.p1 if a else ''}</td><td>{a.d1 if a else ''}</td></tr>
                [cite_start]<tr><td>AUDITIVO [cite: 26]</td><td>{a.p2 if a else ''}</td><td>{a.d2 if a else ''}</td></tr>
                [cite_start]<tr><td>RESPIRATORIOS [cite: 27]</td><td>{a.p3 if a else ''}</td><td>{a.d3 if a else ''}</td></tr>
                [cite_start]<tr><td>CARDIO-VASCULARES [cite: 28]</td><td>{a.p4 if a else ''}</td><td>{a.d4 if a else ''}</td></tr>
                [cite_start]<tr><td>ESTOMAGO/INTESTINO [cite: 29]</td><td>{a.p5 if a else ''}</td><td>{a.d5 if a else ''}</td></tr>
                [cite_start]<tr><td>SANGRE [cite: 29]</td><td>{a.p6 if a else ''}</td><td>{a.d6 if a else ''}</td></tr>
                [cite_start]<tr><td>GENITO/URINARIO [cite: 30]</td><td>{a.p7 if a else ''}</td><td>{a.d7 if a else ''}</td></tr>
                [cite_start]<tr><td>SISTEMA NERVIOSO [cite: 31]</td><td>{a.p8 if a else ''}</td><td>{a.d8 if a else ''}</td></tr>
                [cite_start]<tr><td>PSIQUIATRICOS [cite: 32]</td><td>{a.p9 if a else ''}</td><td>{a.d9 if a else ''}</td></tr>
                [cite_start]<tr><td>OSTEOMUSCULARES [cite: 47]</td><td>{a.p10 if a else ''}</td><td>{a.d10 if a else ''}</td></tr>
            </table>
        </div>
        <div class="page">
            [cite_start]<div class="section">ANTECEDENTES OCUPACIONALES [cite: 87]</div>
            <table class="table">
                [cite_start]<tr style="background:#eee"><td>EDAD INICIO</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP [cite: 90]</td></tr>
                {filas_laboral}
            </table>
            <div class="section">3. [cite_start]HABITOS [cite: 77]</div>
            <table class="table">
                [cite_start]<tr><td>ALCOHOL [cite: 82][cite_start]: {h.h2 if h else ''} ({h.r2 if h else ''})</td><td>TABACO[cite: 83]: {h.h1 if h else ''} ({h.r1 if h else ''})</td></tr>
                [cite_start]<tr><td>DROGAS [cite: 84][cite_start]: {h.h3 if h else ''}</td><td>COCA (BOLO)[cite: 86]: {h.h4 if h else ''}</td></tr>
                [cite_start]<tr><td>DEPORTES [cite: 76][cite_start]: {h.h5 if h else ''}</td><td>GRUPO SANGUINEO[cite: 73]: {h.r10 if h else ''}</td></tr>
            </table>
            <div class="sig">
                <div class="line"></div>
                [cite_start]FIRMA DEL TRABAJADOR [cite: 124]<br>C.I. {p.ci}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
