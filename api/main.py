from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os
from . import models, schemas, crud
from .database import SessionLocal, engine

# Asegura la creación de tablas
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
    data = crud.get_historial_completo(db, paciente_id)
    if not data or not data["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p = data["paciente"]
    f = data.get("filiacion")
    a = data.get("antecedentes")
    h = data.get("habitos")
    
    def mark(val, target):
        if val is None: return ""
        return "X" if str(val).upper() == target else ""

    def get_val(obj, attr, default=""):
        if obj is None: return default
        res = getattr(obj, attr, None)
        # Solo filtramos nulos reales, no el texto "N/A" si es lo que viene de la DB
        if res is None or str(res).lower() in ["none", "null", "undefined"]:
            return default
        return res

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 8mm; }}
            body {{ font-family: 'Arial Narrow', Arial, sans-serif; font-size: 8.5px; line-height: 1.1; color: #000; }}
            .header-table, .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 4px; }}
            .header-table td, .data-table td, .data-table th {{ border: 1px solid black; padding: 2px; }}
            .section-title {{ background-color: #d9e2f3; font-weight: bold; text-align: center; border: 1px solid black; padding: 2px; text-transform: uppercase; font-size: 9px; }}
            .label {{ font-size: 7px; font-weight: normal; color: #333; display: block; text-transform: uppercase; }}
            .value {{ font-weight: bold; text-transform: uppercase; font-size: 9px; }}
            .col-si-no {{ width: 20px; text-align: center; font-weight: bold; font-size: 10px; }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td style="width: 15%; text-align: center;">
                    <img src="https://historial-clinico-nube.onrender.com/LOGO.PNG" width="70" onerror="this.src='https://i.ibb.co/Y7YpLp0/med-logo.png'">
                </td>
                <td style="text-align: center; font-weight: bold; font-size: 13px;">DECLARACIÓN JURADA DE SALUD</td>
            </tr>
        </table>

        <div class="section-title">AFILIACIÓN DEL TRABAJADOR</div>
        <table class="data-table">
            <tr>
                <td colspan="4"><span class="label">1. APELLIDOS Y NOMBRES</span><span class="value">{get_val(p, 'apellidos')} {get_val(p, 'nombres')}</span></td>
            </tr>
            <tr>
                <td style="width: 20%;"><span class="label">2. EDAD</span><span class="value">{get_val(f, 'edad')}</span></td>
                <td style="width: 20%;"><span class="label">3. SEXO</span><span class="value">{get_val(f, 'sexo')}</span></td>
                <td style="width: 30%;"><span class="label">4. FECHA NACIMIENTO</span><span class="value">{get_val(f, 'fecha_nacimiento')}</span></td>
                <td style="width: 30%;"><span class="label">5. LUGAR NACIMIENTO</span><span class="value">{get_val(f, 'lugar_nacimiento')}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">6. DOCUMENTO DE IDENTIDAD</span><span class="value">{get_val(p, 'ci')}</span></td>
                <td colspan="2"><span class="label">7. ESTADO CIVIL</span><span class="value">{get_val(f, 'estado_civil')}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">8. DOMICILIO ACTUAL</span><span class="value">{get_val(f, 'domicilio')} # {get_val(f, 'n_casa')}</span></td>
                <td><span class="label">9. ZONA/BARRIO</span><span class="value">{get_val(f, 'zona_barrio')}</span></td>
                <td><span class="label">10. CIUDAD/PAÍS</span><span class="value">{get_val(f, 'ciudad')}, {get_val(f, 'pais')}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">11. TELÉFONO / CELULAR</span><span class="value">{get_val(f, 'telefono')}</span></td>
                <td colspan="2"><span class="label">12. PROFESIÓN U OFICIO</span><span class="value">{get_val(f, 'profesion_oficio')}</span></td>
            </tr>
        </table>

        <div class="section-title">ANTECEDENTES PATOLÓGICOS</div>
        <table class="data-table">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th>SISTEMA / ÓRGANO / ENFERMEDAD</th>
                    <th class="col-si-no">SI</th>
                    <th class="col-si-no">NO</th>
                    <th>DETALLE / OBSERVACIÓN</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f"<tr><td>{label}</td><td class='col-si-no'>{mark(get_val(a, f'p{i}', None), 'SI')}</td><td class='col-si-no'>{mark(get_val(a, f'p{i}', None), 'NO')}</td><td class='value'>{get_val(a, f'd{i}', '')}</td></tr>" 
                for i, label in enumerate([
                    "1. VISTA (Glaucoma, Retinopatía, otros)", "2. AUDITIVO (Hipoacusia, Vértigo, otros)", 
                    "3. RESPIRATORIO (Asma, Bronquitis, otros)", "4. CARDIO-VASCULARES (HTA, Arritmia)", 
                    "5. ESTÓMAGO/INTESTINO/HÍGADO/PÁNCREAS", "6. SANGRE (Anemia, Coagulopatía)", 
                    "7. GENITO-URINARIO (Infecciones, Quistes)", "8. SISTEMA NERVIOSO (Epilepsia, Mareos)", 
                    "9. PSIQUIÁTRICOS / MENTALES (Depresión, Ansiedad)", "10. OSTEOMUSCULARES (Fracturas, Artralgias)", 
                    "11. ENDOCRINOLÓGICOS (Diabetes, Obesidad)", "12. REUMATOLÓGICOS (Artritis, Lupus)", 
                    "13. GENERALES (Cáncer, Hernias)", "14. DERMATOLÓGICAS (Dermatitis, Micosis)", 
                    "15. ALERGIA (Medicamentos, Alimentos)", "16. INFECCIONES (Hepatitis, TBC, Chagas)", 
                    "17. CIRUGÍAS (Indique cuál y fecha)", "18. ACCIDENTES DE TRABAJO"
                ], 1)])}
                <tr>
                    <td>19. ACCIDENTES PARTICULARES</td>
                    <td class="col-si-no">{mark(get_val(h, 'h8', None), 'SI')}</td>
                    <td class="col-si-no">{mark(get_val(h, 'h8', None), 'NO')}</td>
                    <td class="value">{get_val(h, 'r8', '')}</td>
                </tr>
                <tr>
                    <td>20. MEDICAMENTOS (Uso actual)</td>
                    <td class="col-si-no">{mark(get_val(h, 'h9', None), 'SI')}</td>
                    <td class="col-si-no">{mark(get_val(h, 'h9', None), 'NO')}</td>
                    <td class="value">{get_val(h, 'r9', '')}</td>
                </tr>
                <tr>
                    <td>21. GRUPO SANGUÍNEO</td>
                    <td colspan="2" style="background-color: #eee;"></td>
                    <td class="value">{get_val(h, 'r10', '')}</td>
                </tr>
                <tr>
                    <td>22. DEPORTES (Actividad y frecuencia)</td>
                    <td class="col-si-no">{mark(get_val(h, 'h7', None), 'SI')}</td>
                    <td class="col-si-no">{mark(get_val(h, 'h7', None), 'NO')}</td>
                    <td class="value">{get_val(h, 'r7', '')}</td>
                </tr>
            </tbody>
        </table>
        <script>window.print();</script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
