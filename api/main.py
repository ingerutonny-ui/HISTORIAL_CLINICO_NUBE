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
def generar_reporte(paciente_id: int, db: Session = Depends(get_db)):
    res = crud.get_historial_completo(db, paciente_id)
    p, f, a, h = res["paciente"], res["filiacion"], res["antecedentes"], res["habitos"]
    
    if not p: raise HTTPException(status_code=404, detail="No existe")

    def get_v(obj, attr, default="S/D"):
        val = getattr(obj, attr, None)
        return str(val).upper() if val and str(val).strip() != "" else default

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    # SECCIÓN I: FILIACIÓN
    filiacion_html = f"""
    <table>
        <tr><td colspan="4" class="header">I. AFILIACIÓN DEL TRABAJADOR</td></tr>
        <tr>
            <td style="width:25%"><b>APELLIDOS Y NOMBRES:</b></td>
            <td colspan="3">{get_v(p,'apellidos')} {get_v(p,'nombres')}</td>
        </tr>
        <tr>
            <td><b>EDAD:</b></td><td>{get_v(f,'edad')} AÑOS</td>
            <td><b>SEXO:</b></td><td>{get_v(f,'sexo')}</td>
        </tr>
        <tr>
            <td><b>FECHA NACIMIENTO:</b></td><td>{get_v(f,'fecha_nacimiento')}</td>
            <td><b>LUGAR:</b></td><td>{get_v(f,'lugar_nacimiento')}</td>
        </tr>
        <tr>
            <td><b>C.I.:</b></td><td>{get_v(p,'ci')}</td>
            <td><b>ESTADO CIVIL:</b></td><td>{get_v(f,'estado_civil')}</td>
        </tr>
        <tr>
            <td><b>DOMICILIO:</b></td>
            <td colspan="3">{get_v(f,'domicilio')} NO. {get_v(f,'n_casa')}, BARRIO {get_v(f,'zona_barrio')}</td>
        </tr>
        <tr>
            <td><b>CIUDAD / PAÍS:</b></td><td>{get_v(f,'ciudad')} / {get_v(f,'pais')}</td>
            <td><b>TELÉFONO:</b></td><td>{get_v(f,'telefono')}</td>
        </tr>
        <tr>
            <td><b>PROFESIÓN / LABOR:</b></td><td colspan="3">{get_v(f,'profesion_oficio')}</td>
        </tr>
    </table>
    """

    # SECCIÓN II: ANTECEDENTES
    desc_p2 = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES", "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", "ALERGIA", "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(desc_p2)])

    # SECCIÓN III: HISTORIA LABORAL
    historia_html = "SIN REGISTROS"
    try:
        if h and h.historia_laboral:
            data = json.loads(h.historia_laboral)
            filas = "".join([f"<tr><td>{i.get('edad','-')}</td><td>{i.get('emp','-')}</td><td>{i.get('ocu','-')}</td><td>{i.get('tie','-')}</td><td>{i.get('rie','-')}</td><td>{i.get('epp','-')}</td></tr>" for i in data])
            historia_html = f"<table><tr class='header'><td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td></tr>{filas}</table>"
    except: historia_html = "ERROR"

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    body {{ font-family: Arial; font-size: 8px; line-height: 1.1; text-transform: uppercase; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
    td, th {{ border: 1px solid black; padding: 3px; }}
    .header {{ background: #d9e2f3; font-weight: bold; text-align: center; }}
    </style></head><body>
    <div style="text-align:center; font-weight:bold; font-size:12px; margin-bottom:10px;">DECLARACIÓN JURADA DE SALUD</div>
    {filiacion_html}
    <table>
        <tr class="header"><td>II. ANTECEDENTES</td><td>SI</td><td>NO</td><td>DETALLES</td></tr>
        {rows_p2}
        <tr><td>19. ACCIDENTES PARTICULARES</td><td>{mark(h,'accidentes_si_no','SI')}</td><td>{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
        <tr><td>20. MEDICAMENTOS (ACTUAL)</td><td>{mark(h,'medicamentos_si_no','SI')}</td><td>{mark(h,'medicamentos_si_no','NO')}</td><td>{get_v(h,'medicamentos_detalle')}</td></tr>
        <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2"></td><td>{get_v(h,'grupo_sanguineo')}</td></tr>
        <tr><td>22. DEPORTES</td><td>{mark(h,'deportes_si_no','SI')}</td><td>{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle')}</td></tr>
    </table>
    <div class="header">III. HISTORIA LABORAL</div>
    {historia_html}
    <div class="header">IV. RIESGOS EXPUESTOS DURANTE VIDA LABORAL</div>
    <div style="border:1px solid black; padding:5px;">{get_v(h, 'riesgos_vida_laboral')}</div>
    <div style="margin-top:15px; display:flex; justify-content:space-between;"><span>FECHA: 06/02/2026</span><span>FIRMA: _________________</span></div>
    <script>window.print();</script></body></html>
    """
    return HTMLResponse(content=html)
