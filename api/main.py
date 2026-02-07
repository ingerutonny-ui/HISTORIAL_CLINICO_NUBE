from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List  # <--- ESTA LÍNEA CORRIGE EL ERROR DE RENDER
import json
from . import models, schemas, crud
from .database import SessionLocal, engine

# Sincronización automática de base de datos y migración de columnas faltantes
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

# Configuración de CORS para permitir la conexión desde GitHub Pages
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
    p, f, a, h = res["paciente"], res["filiacion"], res["antecedentes"], res["habitos"]
    
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

    # Lógica de Antecedentes (Sección II)
    labels = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", 
              "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES", 
              "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", "ALERGIA", 
              "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels)])

    # Lógica de Historia Laboral (Sección III)
    filas_h = "<tr><td colspan='6' style='text-align:center;'>SIN REGISTROS</td></tr>"
    if h and h.historia_laboral:
        try:
            items = json.loads(h.historia_laboral)
            if items:
                filas_h = "".join([f"<tr><td>{i.get('edad','-')}</td><td>{i.get('emp','-')}</td><td>{i.get('ocu','-')}</td><td>{i.get('tie','-')}</td><td>{i.get('rie','-')}</td><td>{i.get('epp','-')}</td></tr>" for i in items])
        except Exception:
            pass

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
        @media print {{ .page-break {{ page-break-before: always; }} }}
        body {{ font-family: 'Arial Narrow', Arial; font-size: 10px; text-transform: uppercase; margin: 0; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
        td {{ border: 1px solid black; padding: 5px; }}
        .header {{ background: #d9e2f3; font-weight: bold; text-align: center; font-size: 11px; }}
        .title {{ text-align: center; font-size: 14px; font-weight: bold; margin-bottom: 20px; }}
    </style></head><body>
        <div class="title">DECLARACIÓN JURADA DE SALUD - {get_v(p,'apellidos')} {get_v(p,'nombres')}</div>
        <table>
            <tr><td colspan="4" class="header">I. AFILIACIÓN DEL TRABAJADOR</td></tr>
            <tr><td width="20%"><b>NOMBRES:</b></td><td colspan="3">{get_v(p,'apellidos')} {get_v(p,'nombres')}</td></tr>
            <tr><td><b>EDAD:</b></td><td>{get_v(f,'edad')} AÑOS</td><td width="20%"><b>SEXO:</b></td><td>{get_v(f,'sexo')}</td></tr>
            <tr><td><b>FECHA NAC.:</b></td><td>{get_v(f,'fecha_nacimiento')}</td><td><b>C.I.:</b></td><td>{get_v(p,'ci')}</td></tr>
            <tr><td><b>DOMICILIO:</b></td><td colspan="3">{get_v(f,'domicilio')} NO. {get_v(f,'n_casa')}, {get_v(f,'zona_barrio')}</td></tr>
            <tr><td><b>CIUDAD/PAÍS:</b></td><td>{get_v(f,'ciudad')} / {get_v(f,'pais')}</td><td><b>TELÉFONO:</b></td><td>{get_v(f,'telefono')}</td></tr>
            <tr><td><b>PROFESIÓN:</b></td><td colspan="3">{get_v(f,'profesion_oficio')}</td></tr>
        </table>
        <table>
            <tr class="header"><td>II. ANTECEDENTES</td><td width="40px">SI</td><td width="40px">NO</td><td>DETALLES / OBSERVACIONES</td></tr>
            {rows_p2}
        </table>
        <div class="page-break"></div>
        <table>
            <tr class="header"><td colspan="4">III. HÁBITOS Y OTROS ANTECEDENTES</td></tr>
            <tr><td width="30%">FUMA</td><td>{get_v(h,'fuma_si_no')}</td><td width="20%">CANTIDAD:</td><td>{get_v(h,'fuma_detalle')}</td></tr>
            <tr><td>ALCOHOL</td><td>{get_v(h,'alcohol_si_no')}</td><td>FRECUENCIA:</td><td>{get_v(h,'alcohol_detalle')}</td></tr>
            <tr><td>DROGAS</td><td>{get_v(h,'drogas_si_no')}</td><td>TIPO:</td><td>{get_v(h,'drogas_detalle')}</td></tr>
            <tr><td>PIJCHAR (COCA)</td><td colspan="3">{get_v(h,'pijchar_si_no')}</td></tr>
            <tr><td>DEPORTES</td><td>{get_v(h,'deportes_si_no')}</td><td>CUAL:</td><td>{get_v(h,'deportes_detalle')}</td></tr>
            <tr><td>GRUPO SANGUÍNEO</td><td colspan="3"><b>{get_v(h,'grupo_sanguineo')}</b></td></tr>
            <tr><td>ACCIDENTES TRABAJO</td><td>{get_v(h,'accidentes_si_no')}</td><td>DETALLE:</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
            <tr><td>MEDICAMENTOS</td><td>{get_v(h,'medicamentos_si_no')}</td><td>DETALLE:</td><td>{get_v(h,'medicamentos_detalle')}</td></tr>
        </table>
        <div class="header" style="border:1px solid black;">IV. ANTECEDENTES OCUPACIONALES (HISTORIA LABORAL)</div>
        <table>
            <tr class="header" style="font-size:9px;"><td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td></tr>
            {filas_h}
        </table>
        <div class="header" style="border:1px solid black; margin-top:10px;">V. RIESGOS EXPUESTOS DURANTE VIDA LABORAL</div>
        <div style="border:1px solid black; padding:15px; min-height:60px; font-size:11px;">{get_v(h, 'riesgos_vida_laboral')}</div>
        <div style="display:flex; justify-content: space-around; margin-top:50px;">
            <div style="text-align:center; border-top:1px solid black; width:200px;">FIRMA DEL TRABAJADOR</div>
            <div style="text-align:center; border-top:1px solid black; width:200px;">HUELLA DIGITAL</div>
        </div>
        <script>window.print();</script>
    </body></html>
    """
    return HTMLResponse(content=html)
