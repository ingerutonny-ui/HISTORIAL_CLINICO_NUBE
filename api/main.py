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

    def get_v(obj, attr, default="N/A"):
        val = getattr(obj, attr, None)
        return str(val).upper() if val and str(val).strip() != "" else default

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    # PROCESAMIENTO DE HISTORIA LABORAL (Elimina las comillas y crea tabla)
    historia_html = "SIN REGISTROS"
    try:
        if h and h.historia_laboral:
            data_laboral = json.loads(h.historia_laboral)
            filas_laboral = "".join([f"""
                <tr>
                    <td>{item.get('EDAD','-')}</td>
                    <td>{item.get('EMP','-')}</td>
                    <td>{item.get('OCU','-')}</td>
                    <td>{item.get('TIE','-')}</td>
                    <td>{item.get('RIE','-')}</td>
                    <td>{item.get('EPP','-')}</td>
                </tr>""" for item in data_laboral])
            historia_html = f"""
                <table style='margin-top:0;'>
                    <tr style='background:#f2f2f2; font-weight:bold; text-align:center;'>
                        <td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td>
                    </tr>
                    {filas_laboral}
                </table>"""
    except:
        historia_html = get_v(h, 'historia_laboral')

    labels_p2 = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", 
                 "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES",
                 "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", 
                 "ALERGIA", "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels_p2)])

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    body {{ font-family: Arial; font-size: 9px; line-height: 1.2; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    td, th {{ border: 1px solid black; padding: 4px; }}
    .header {{ background: #d9e2f3; font-weight: bold; text-align: center; padding: 5px; text-transform: uppercase; }}
    </style></head><body>
    <div class="header">DECLARACIÓN JURADA DE SALUD - {get_v(p, 'apellidos')} {get_v(p, 'nombres')}</div>
    <table>
        <tr class="header"><td style="width:40%">SISTEMA / ANTECEDENTE</td><td style="width:30px">SI</td><td style="width:30px">NO</td><td>OBSERVACIONES / DETALLES</td></tr>
        {rows_p2}
        <tr><td>19. ACCIDENTES PARTICULARES</td><td style="text-align:center;">{mark(h,'accidentes_si_no','SI')}</td><td style="text-align:center;">{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
        <tr><td>20. MEDICAMENTOS (Uso actual)</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','SI')}</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','NO')}</td><td>{get_v(h,'medicamentos_detalle')}</td></tr>
        <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2" style="background:#f2f2f2;"></td><td><b>{get_v(h,'grupo_sanguineo')}</b></td></tr>
        <tr><td>22. DEPORTES</td><td style="text-align:center;">{mark(h,'deportes_si_no','SI')}</td><td style="text-align:center;">{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle')}</td></tr>
    </table>
    <div class="header">HISTORIA LABORAL (ÚLTIMOS EMPLEOS)</div>
    {historia_html}
    <div style="margin-top:20px; text-align:center; font-size:8px; color:#666;">Documento generado digitalmente - Proyecto HISTORIAL_CLINICO_NUBE</div>
    <script>window.print();</script></body></html>
    """
    return HTMLResponse(content=html)
