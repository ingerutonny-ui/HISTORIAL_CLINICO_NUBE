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

    def get_v(obj, attr, default="NORMAL"):
        val = getattr(obj, attr, None)
        return str(val).upper() if val and str(val).strip() != "" else default

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    labels_p2 = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", 
                 "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES",
                 "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", 
                 "ALERGIA", "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels_p2)])

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    body {{ font-family: Arial; font-size: 9px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
    td, th {{ border: 1px solid black; padding: 3px; }}
    .header {{ background: #d9e2f3; font-weight: bold; text-align: center; }}
    </style></head><body>
    <div class="header">DECLARACIÓN JURADA DE SALUD - {get_v(p, 'apellidos')} {get_v(p, 'nombres')}</div>
    <table>
        <tr class="header"><td>SISTEMA</td><td style="width:25px">SI</td><td style="width:25px">NO</td><td>OBSERVACIONES</td></tr>
        {rows_p2}
        <tr><td>19. ACCIDENTES PARTICULARES</td><td style="text-align:center;">{mark(h,'accidentes_si_no','SI')}</td><td style="text-align:center;">{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle','NINGUNO')}</td></tr>
        <tr><td>20. MEDICAMENTOS (Uso actual)</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','SI')}</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','NO')}</td><td>{get_v(h,'medicamentos_detalle','NINGUNO')}</td></tr>
        <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2"></td><td>{get_v(h,'grupo_sanguineo','S/D')}</td></tr>
        <tr><td>22. DEPORTES</td><td style="text-align:center;">{mark(h,'deportes_si_no','SI')}</td><td style="text-align:center;">{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle','NINGUNO')}</td></tr>
    </table>
    <div class="header">HISTORIA LABORAL</div>
    <div style="border:1px solid black; padding:5px;">{get_v(h, 'historia_laboral', 'SIN REGISTRO')}</div>
    <script>window.print();</script></body></html>
    """
    return HTMLResponse(content=html)
