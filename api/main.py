from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import json
from . import models, schemas, crud
from .database import SessionLocal, engine

# Sincronización de base de datos y creación de columnas si no existen
models.Base.metadata.create_all(bind=engine)
with engine.begin() as conn:
    columnas = ["fuma_si_no", "fuma_detalle", "alcohol_si_no", "alcohol_detalle", 
                "drogas_si_no", "drogas_detalle", "pijchar_si_no"]
    for col in columnas:
        try:
            conn.execute(text(f"ALTER TABLE habitos_p3 ADD COLUMN {col} TEXT"))
        except Exception:
            pass

app = FastAPI()

# CONFIGURACIÓN DE CORS: Permite que GitHub Pages se conecte
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
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db)

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
    p = res["paciente"]
    f = res["filiacion"]
    a = res["antecedentes"]
    h = res["habitos"]
    
    if not p:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    def get_v(obj, attr, default="---"):
        val = getattr(obj, attr, None)
        if val is None or str(val).strip() == "" or str(val).upper() == "NONE":
            return default
        return str(val).upper()

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    labels = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", 
              "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES", 
              "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", "ALERGIA", 
              "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels)])

    filas_h = "<tr><td colspan='6' style='text-align:center;'>SIN REGISTROS</td></tr>"
    if h and h.historia_laboral:
        try:
            items = json.loads(h.historia_laboral)
            if items:
                filas_h = "".join([f"<tr><td>{i.get('edad','-')}</td><td>{i.get('emp','-')}</td><td>{i.get('ocu','-')}</td><td>{i.get('tie','-')}</td><td>{i.get('rie','-')}</td><td>{i.get('epp','-')}</td></tr>" for i in items])
        except: pass

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
        @media print {{ .page-break {{ page-break-before: always; }} }}
        body {{ font-family: Arial; font-size: 10px; text-transform: uppercase; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
        td {{ border: 1px solid black; padding: 4px; }}
        .header {{ background: #d9e2f3; font-weight: bold; text-align: center; }}
    </style></head><body>
        <h3 style="text-align:center;">DECLARACIÓN JURADA DE SALUD - {get_v(p,'apellidos')} {get_v(p,'nombres')}</h3>
        <table>
            <tr><td colspan="4" class="header">I. AFILIACIÓN</td></tr>
            <tr><td>NOMBRES:</td><td colspan="3">{get_v(p,'apellidos')} {get_v(p,'nombres')}</td></tr>
            <tr><td>EDAD:</td><td>{get_v(f,'edad')}</td><td>SEXO:</td><td>{get_v(f,'sexo')}</td></tr>
            <tr><td>CI:</td><td>{get_v(p,'ci')}</td><td>TELÉFONO:</td><td>{get_v(f,'telefono')}</td></tr>
        </table>
        <table>
            <tr class="header"><td>II. ANTECEDENTES</td><td width="30">SI</td><td width="30">NO</td><td>DETALLES</td></tr>
            {rows_p2}
        </table>
        <div class="page-break"></div>
        <table>
            <tr class="header"><td colspan="4">III. HÁBITOS</td></tr>
            <tr><td>FUMA</td><td>{get_v(h,'fuma_si_no')}</td><td>CANTIDAD:</td><td>{get_v(h,'fuma_detalle')}</td></tr>
            <tr><td>ALCOHOL</td><td>{get_v(h,'alcohol_si_no')}</td><td>FRECUENCIA:</td><td>{get_v(h,'alcohol_detalle')}</td></tr>
            <tr><td>DROGAS</td><td>{get_v(h,'drogas_si_no')}</td><td>TIPO:</td><td>{get_v(h,'drogas_detalle')}</td></tr>
            <tr><td>PIJCHAR</td><td>{get_v(h,'pijchar_si_no')}</td><td>DEPORTES:</td><td>{get_v(h,'deportes_detalle')}</td></tr>
            <tr><td>GRUPO SANGUÍNEO</td><td colspan="3">{get_v(h,'grupo_sanguineo')}</td></tr>
        </table>
        <div class="header" style="border:1px solid black;">IV. HISTORIA LABORAL</div>
        <table>
            <tr class="header"><td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td></tr>
            {filas_h}
        </table>
        <div class="header" style="border:1px solid black; margin-top:10px;">V. RIESGOS EXPUESTOS</div>
        <div style="border:1px solid black; padding:10px;">{get_v(h, 'riesgos_vida_laboral')}</div>
        <script>window.print();</script>
    </body></html>
    """
    return HTMLResponse(content=html)
