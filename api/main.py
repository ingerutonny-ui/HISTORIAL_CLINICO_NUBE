from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from . import models, schemas, crud
from .database import SessionLocal, engine

# Sincronización automática de la base de datos
models.Base.metadata.create_all(bind=engine)
with engine.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE habitos_p3 ADD COLUMN riesgos_vida_laboral TEXT"))
    except:
        pass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pacientes/", response_model=list[schemas.Paciente])
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
        raise HTTPException(status_code=404)

    def get_v(obj, attr, default="S/D"):
        val = getattr(obj, attr, None)
        return str(val).upper() if val and str(val).strip() != "" else default

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    labels = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES", "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", "ALERGIA", "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels)])

    filas_h = "<tr><td colspan='6'>SIN DATOS</td></tr>"
    if h and h.historia_laboral:
        try:
            items = json.loads(h.historia_laboral)
            filas_h = "".join([f"<tr><td>{i.get('edad','-')}</td><td>{i.get('emp','-')}</td><td>{i.get('ocu','-')}</td><td>{i.get('tie','-')}</td><td>{i.get('rie','-')}</td><td>{i.get('epp','-')}</td></tr>" for i in items])
        except:
            pass

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    body {{ font-family: Arial; font-size: 8px; text-transform: uppercase; padding: 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    td {{ border: 1px solid black; padding: 4px; }}
    .bg {{ background: #d9e2f3; font-weight: bold; text-align: center; }}
    </style></head><body>
    <div style="text-align:center; font-weight:bold; font-size:12px;">DECLARACIÓN JURADA DE SALUD - {get_v(p,'apellidos')} {get_v(p,'nombres')}</div>
    <table>
        <tr><td colspan="4" class="bg">I. AFILIACIÓN</td></tr>
        <tr><td><b>NOMBRE:</b></td><td colspan="3">{get_v(p,'apellidos')} {get_v(p,'nombres')}</td></tr>
        <tr><td><b>EDAD:</b></td><td>{get_v(f,'edad')}</td><td><b>FECHA NAC.:</b></td><td>{get_v(f,'fecha_nacimiento')}</td></tr>
        <tr><td><b>C.I.:</b></td><td>{get_v(p,'ci')}</td><td><b>DOMICILIO:</b></td><td>{get_v(f,'domicilio')} {get_v(f,'n_casa')}, {get_v(f,'zona_barrio')}</td></tr>
        <tr><td><b>CIUDAD/PAÍS:</b></td><td>{get_v(f,'ciudad')} / {get_v(f,'pais')}</td><td><b>PROFESIÓN:</b></td><td>{get_v(f,'profesion_oficio')}</td></tr>
    </table>
    <table><tr class="bg"><td>II. ANTECEDENTES</td><td>SI</td><td>NO</td><td>OBSERVACIONES</td></tr>{rows_p2}
    <tr><td>19. ACCIDENTES</td><td>{mark(h,'accidentes_si_no','SI')}</td><td>{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
    <tr><td>20. MEDICAMENTOS</td><td>{mark(h,'medicamentos_si_no','SI')}</td><td>{mark(h,'medicamentos_si_no','NO')}</td><td>{get_v(h,'medicamentos_detalle')}</td></tr>
    <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2"></td><td>{get_v(h,'grupo_sanguineo')}</td></tr>
    <tr><td>22. DEPORTES</td><td>{mark(h,'deportes_si_no','SI')}</td><td>{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle')}</td></tr>
    </table>
    <div class="bg" style="border:1px solid black;">III. HISTORIA LABORAL</div>
    <table><tr class="bg"><td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td></tr>{filas_h}</table>
    <div class="bg" style="border:1px solid black; margin-top:5px;">IV. RIESGOS EXPUESTOS</div>
    <div style="border:1px solid black; padding:10px; min-height:30px;">{get_v(h, 'riesgos_vida_laboral')}</div>
    <script>window.print();</script></body></html>"""
    return HTMLResponse(content=html)
