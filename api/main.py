from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear tablas y forzar columna de riesgos si no existe
models.Base.metadata.create_all(bind=engine)
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE habitos_p3 ADD COLUMN riesgos_vida_laboral VARCHAR"))
        conn.commit()
    except:
        pass 

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

# RUTA PARA REGISTRO INICIAL (Soluciona el 404 de tu captura)
@app.post("/pacientes/")
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

    def get_v(obj, attr, default="N/A"):
        val = getattr(obj, attr, None)
        return str(val).upper() if val and str(val).strip() != "" else default

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    # Lógica de Historia Laboral
    h_html = "<tr><td colspan='6' style='text-align:center;'>SIN REGISTROS</td></tr>"
    if h and h.historia_laboral:
        try:
            data_laboral = json.loads(h.historia_laboral)
            filas = ""
            for x in data_laboral:
                filas += f"""
                <tr>
                    <td>{x.get('edad','-')}</td>
                    <td>{x.get('emp','-')}</td>
                    <td>{x.get('ocu','-')}</td>
                    <td>{x.get('tie','-')}</td>
                    <td>{x.get('rie','-')}</td>
                    <td>{x.get('epp','-')}</td>
                </tr>"""
            h_html = filas
        except:
            pass

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 9px; text-transform: uppercase; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
        td {{ border: 1px solid #000; padding: 5px; }}
        .bg-blue {{ background-color: #d9e2f3; font-weight: bold; text-align: center; }}
        .title {{ text-align: center; font-size: 14px; font-weight: bold; text-decoration: underline; margin-bottom: 15px; }}
    </style></head><body>
    <div class="title">DECLARACIÓN JURADA DE SALUD - {get_v(p, 'apellidos')} {get_v(p, 'nombres')}</div>
    
    <table>
        <tr><td colspan="4" class="bg-blue">I. AFILIACIÓN DEL TRABAJADOR</td></tr>
        <tr><td><b>APELLIDOS Y NOMBRES:</b></td><td colspan="3">{get_v(p, 'apellidos')} {get_v(p, 'nombres')}</td></tr>
        <tr><td><b>EDAD:</b></td><td>{get_v(f, 'edad')} AÑOS</td><td><b>FECHA NACIMIENTO:</b></td><td>{get_v(f, 'fecha_nacimiento')}</td></tr>
        <tr><td><b>C.I.:</b></td><td>{get_v(p, 'ci')}</td><td><b>DOMICILIO:</b></td><td>{get_v(f, 'domicilio')} NO. {get_v(f, 'n_casa')}, BARRIO {get_v(f, 'zona_barrio')}</td></tr>
        <tr><td><b>CIUDAD / PAÍS:</b></td><td>{get_v(f, 'ciudad')} / {get_v(f, 'pais')}</td><td><b>PROFESIÓN / LABOR:</b></td><td>{get_v(f, 'profesion_oficio')}</td></tr>
    </table>

    <table>
        <tr class="bg-blue"><td>SISTEMA / ANTECEDENTE</td><td>SI</td><td>NO</td><td>OBSERVACIONES / DETALLES</td></tr>
        <tr><td>1. VISTA</td><td>{mark(a,'p1','SI')}</td><td>{mark(a,'p1','NO')}</td><td>{get_v(a,'d1')}</td></tr>
        <tr><td>2. AUDITIVO</td><td>{mark(a,'p2','SI')}</td><td>{mark(a,'p2','NO')}</td><td>{get_v(a,'d2')}</td></tr>
        <tr><td>18. ACCIDENTES DE TRABAJO</td><td>{mark(h,'accidentes_si_no','SI')}</td><td>{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
        <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2"></td><td>{get_v(h,'grupo_sanguineo')}</td></tr>
        <tr><td>22. DEPORTES</td><td>{mark(h,'deportes_si_no','SI')}</td><td>{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle')}</td></tr>
    </table>

    <div class="bg-blue" style="border: 1px solid black;">HISTORIA LABORAL (ÚLTIMOS EMPLEOS)</div>
    <table>
        <tr style="font-weight:bold; text-align:center;">
            <td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td>
        </tr>
        {h_html}
    </table>

    <div class="bg-blue" style="border: 1px solid black;">III. RIESGOS EXPUESTOS DURANTE VIDA LABORAL</div>
    <div style="border: 1px solid black; padding: 10px; min-height: 30px;">
        {get_v(h, 'riesgos_vida_laboral')}
    </div>

    <p style="text-align:center; font-size:7px; color:gray; margin-top:20px;">Documento generado digitalmente - Proyecto HISTORIAL_CLINICO_NUBE</p>
    <script>window.print();</script>
    </body></html>
    """
    return HTMLResponse(content=html)
