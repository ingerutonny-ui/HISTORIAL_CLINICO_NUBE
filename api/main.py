from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

# Asegura la creación de tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CONFIGURACIÓN CORS
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
    data = crud.get_historial_completo(db, paciente_id)
    if not data or not data["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p = data["paciente"]
    f = data.get("filiacion")
    a = data.get("antecedentes")
    
    # Función auxiliar para marcar SI/NO
    def mark(val, target):
        return "X" if str(val).upper() == target else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 10mm; }}
            body {{ font-family: 'Arial Narrow', Arial, sans-serif; font-size: 9px; line-height: 1.2; }}
            .header-table, .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
            .header-table td, .data-table td, .data-table th {{ border: 1px solid black; padding: 3px; }}
            .section-title {{ background-color: #d9e2f3; font-weight: bold; text-align: center; border: 1px solid black; padding: 2px; text-transform: uppercase; }}
            .label {{ font-size: 7px; font-weight: normal; color: #444; display: block; }}
            .value {{ font-weight: bold; text-transform: uppercase; font-size: 9px; }}
            .col-si-no {{ width: 25px; text-align: center; font-weight: bold; }}
            .instruction {{ font-size: 8px; font-weight: bold; text-align: center; padding: 4px; border: 1px solid black; }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td style="width: 15%; text-align: center;"><img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="35"></td>
                <td style="text-align: center; font-weight: bold; font-size: 14px;">DECLARACIÓN JURADA DE SALUD</td>
            </tr>
        </table>

        <div class="instruction">Por favor lea con cuidado y escriba con letra clara.</div>
        
        <div class="section-title">AFILIACIÓN DEL TRABAJADOR</div>
        <table class="data-table">
            <tr>
                <td colspan="4"><span class="label">APELLIDOS Y NOMBRES</span><span class="value">{p.apellidos} {p.nombres}</span></td>
            </tr>
            <tr>
                <td style="width: 25%;"><span class="label">EDAD</span><span class="value">{f.edad if f else ''}</span></td>
                <td style="width: 25%; text-align: center;"><span class="label">SEXO</span><span class="value">{f.sexo if f else ''}</span></td>
                <td colspan="2"><span class="label">DOCUMENTO DE IDENTIDAD</span><span class="value">{p.ci}</span></td>
            </tr>
        </table>

        <div class="instruction" style="background-color: #eee;">Indique (SI) o (NO) si usted fue diagnosticado de alguna de las enfermedades:</div>
        
        <table class="data-table">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th>SISTEMA / ÓRGANO</th>
                    <th class="col-si-no">SI</th>
                    <th class="col-si-no">NO</th>
                    <th>DETALLE / OBSERVACIÓN</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>VISTA (Disminución, Glaucoma, otros)</td>
                    <td class="col-si-no">{mark(a.p1, 'SI') if a else ''}</td>
                    <td class="col-si-no">{mark(a.p1, 'NO') if a else ''}</td>
                    <td class="value">{a.d1 if a else ''}</td>
                </tr>
                <tr>
                    <td>AUDITIVO (Hipoacusia, Vértigo, otros)</td>
                    <td class="col-si-no">{mark(a.p2, 'SI') if a else ''}</td>
                    <td class="col-si-no">{mark(a.p2, 'NO') if a else ''}</td>
                    <td class="value">{a.d2 if a else ''}</td>
                </tr>
                <tr>
                    <td>RESPIRATORIO (Asma, Bronquitis, otros)</td>
                    <td class="col-si-no">{mark(a.p3, 'SI') if a else ''}</td>
                    <td class="col-si-no">{mark(a.p3, 'NO') if a else ''}</td>
                    <td class="value">{a.d3 if a else ''}</td>
                </tr>
                <tr>
                    <td>CARDIO-VASCULARES (Hipertensión, Arritmia)</td>
                    <td class="col-si-no">{mark(a.p4, 'SI') if a else ''}</td>
                    <td class="col-si-no">{mark(a.p4, 'NO') if a else ''}</td>
                    <td class="value">{a.d4 if a else ''}</td>
                </tr>
                <tr>
                    <td>SANGRE (Anemia, Coagulopatía, otros)</td>
                    <td class="col-si-no">{mark(a.p6, 'SI') if a else ''}</td>
                    <td class="col-si-no">{mark(a.p6, 'NO') if a else ''}</td>
                    <td class="value">{a.d6 if a else ''}</td>
                </tr>
            </tbody>
        </table>

        <script>window.print();</script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
