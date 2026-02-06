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
            for item in lista_lab:
                filas_laboral += f"<tr><td>{item.get('edad','')}</td><td>{item.get('emp','')}</td><td>{item.get('ocu','')}</td><td>{item.get('tie','')}</td><td>{item.get('rie','')}</td><td>{item.get('epp','')}</td></tr>"
        except:
            pass
    
    while filas_laboral.count("<tr>") < 6:
        filas_laboral += "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 0; }}
            body {{ font-family: Arial, sans-serif; font-size: 8px; margin: 0; padding: 0; text-transform: uppercase; line-height: 1.1; }}
            .page {{ width: 216mm; height: 279mm; padding: 10mm; box-sizing: border-box; page-break-after: always; }}
            .header-box {{ border: 1px solid #000; display: flex; text-align: center; }}
            .logo-area {{ width: 15%; font-weight: bold; font-size: 16px; border-right: 1px solid #000; padding: 5px; display: flex; align-items: center; justify-content: center; }}
            .title-area {{ width: 70%; padding: 5px; }}
            .code-area {{ width: 15%; border-left: 1px solid #000; padding: 5px; }}
            .section-title {{ background: #000; color: #fff; padding: 3px; font-weight: bold; margin-top: 8px; border: 1px solid #000; font-size: 9px; }}
            .grid-table {{ width: 100%; border-collapse: collapse; margin-top: 0px; }}
            .grid-table td {{ border: 1px solid #000; padding: 3px; vertical-align: top; }}
            .label {{ font-size: 6px; font-weight: bold; display: block; }}
            .footer-legal {{ margin-top: 10px; text-align: justify; border: 1px solid #000; padding: 8px; font-size: 7px; }}
            .sig-box {{ margin-top: 25px; text-align: center; }}
            .line {{ border-top: 1px solid #000; width: 200px; margin: 0 auto; padding-top: 2px; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header-box">
                <div class="logo-area">OHS</div>
                <div class="title-area"><b>DECLARACIÓN JURADA DE SALUD</b><br>TRABAJO SANO, SEGURO Y PRODUCTIVO</div>
                <div class="code-area"><span class="label">CÓDIGO</span><b>{p.codigo_paciente}</b></div>
            </div>

            <div class="section-title">1. AFILIACIÓN DEL TRABAJADOR</div>
            <table class="grid-table">
                <tr><td colspan="3"><span class="label">Apellidos y Nombres</span><b>{p.nombres} {p.apellidos}</b></td><td colspan="2"><span class="label">C.I.</span>{p.ci}</td></tr>
                <tr><td><span class="label">Edad</span>{f.edad if f else ''} Años</td><td><span class="label">Sexo</span>{f.sexo if f else ''}</td><td><span class="label">F. Nacimiento</span>{f.fecha_nacimiento if f else ''}</td><td colspan="2"><span class="label">Teléfono</span>{f.telefono if f else ''}</td></tr>
                <tr><td colspan="3"><span class="label">Domicilio</span>{f.domicilio if f else ''} #{f.n_casa if f else ''}</td><td colspan="2"><span class="label">Ciudad/País</span>{f.ciudad if f else ''}</td></tr>
            </table>

            <div class="section-title">2. ANTECEDENTES PATOLÓGICOS</div>
            <table class="grid-table">
                <tr style="background:#eee; font-weight:bold;"><td>SISTEMA / ENFERMEDAD</td><td>SI/NO</td><td>DETALLES / OBSERVACIONES</td></tr>
                <tr><td>VISTA (Glaucoma, Miopía, Pterigión)</td><td>{a.p1 if a else ''}</td><td>{a.d1 if a else ''}</td></tr>
                <tr><td>AUDITIVO (Sordera, Vértigo, Otitis)</td><td>{a.p2 if a else ''}</td><td>{a.d2 if a else ''}</td></tr>
                <tr><td>RESPIRATORIOS (Asma, TBC, Bronquitis)</td><td>{a.p3 if a else ''}</td><td>{a.d3 if a else ''}</td></tr>
                <tr><td>CARDIOVASCULARES (HTA, Soplos, Infartos)</td><td>{a.p4 if a else ''}</td><td>{a.d4 if a else ''}</td></tr>
                <tr><td>DIGESTIVOS (Gastritis, Úlceras)</td><td>{a.p5 if a else ''}</td><td>{a.d5 if a else ''}</td></tr>
                <tr><td>SANGRE (Anemia, Diabetes)</td><td>{a.p6 if a else ''}</td><td>{a.d6 if a else ''}</td></tr>
                <tr><td>GENITOURINARIO (Cálculos, Próstata)</td><td>{a.p7 if a else ''}</td><td>{a.d7 if a else ''}</td></tr>
                <tr><td>SISTEMA NERVIOSO / PSIQUIÁTRICO</td><td>{a.p8 if a else ''}</td><td>{a.d8 if a else ''}</td></tr>
                <tr><td>OSTEOMUSCULARES (Fracturas, Hernias)</td><td>{a.p10 if a else ''}</td><td>{a.d10 if a else ''}</td></tr>
                <tr><td>ALERGIAS / PIEL</td><td>{a.p12 if a else ''}</td><td>{a.d12 if a else ''}</td></tr>
            </table>
        </div>

        <div class="page">
            <div class="section-title">ANTECEDENTES OCUPACIONALES (HISTORIA LABORAL)</div>
            <table class="grid-table">
                <tr style="background:#eee; font-weight:bold; text-align:center;">
                    <td style="width:10%">EDAD</td><td style="width:25%">EMPRESA</td><td style="width:20%">OCUPACIÓN</td><td style="width:15%">TIEMPO</td><td style="width:20%">RIESGOS</td><td style="width:10%">EPP</td>
                </tr>
                {filas_laboral}
            </table>

            <div class="section-title">3. HÁBITOS Y RIESGOS EXPUESTOS</div>
            <table class="grid-table">
                <tr>
                    <td><b>TABACO:</b> {h.h1 if h else ''} ({h.r1 if h else ''})</td>
                    <td><b>ALCOHOL:</b> {h.h2 if h else ''} ({h.r2 if h else ''})</td>
                    <td><b>DROGAS:</b> {h.h3 if h else ''}</td>
                </tr>
                <tr>
                    <td><b>COCA (BOLO):</b> {h.h4 if h else ''}</td>
                    <td><b>DEPORTES:</b> {h.h5 if h else ''} ({h.r5 if h else ''})</td>
                    <td><b>GRUPO SANGUÍNEO:</b> {h.r10 if h else ''}</td>
                </tr>
                <tr>
                    <td colspan="3"><b>RIESGOS LABORALES IDENTIFICADOS DURANTE SU VIDA:</b><br>{h.r6 if h else ''}</td>
                </tr>
            </table>

            <div class="footer-legal">
                POR MEDIO DE ESTE DOCUMENTO MÉDICO LEGAL DECLARO QUE ES VERDAD TODA LA INFORMACIÓN PROPORCIONADA. CUALQUIER OMISIÓN O FALSEDAD INVALIDA EL PRESENTE DE ACUERDO A NORMATIVA DEL MINISTERIO DE SALUD Y POLÍTICAS DE LA EMPRESA.
            </div>

            <div class="sig-box">
                <div class="line">FIRMA DEL TRABAJADOR / PACIENTE</div>
                C.I. {p.ci}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
