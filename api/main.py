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
    
    def mark(val, target):
        return "X" if str(val).upper() == target else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 8mm; }}
            body {{ font-family: 'Arial Narrow', Arial, sans-serif; font-size: 8.5px; line-height: 1.1; }}
            .header-table, .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
            .header-table td, .data-table td, .data-table th {{ border: 1px solid black; padding: 2px; }}
            .section-title {{ background-color: #d9e2f3; font-weight: bold; text-align: center; border: 1px solid black; padding: 2px; text-transform: uppercase; font-size: 9px; }}
            .label {{ font-size: 7px; font-weight: normal; color: #333; display: block; text-transform: uppercase; }}
            .value {{ font-weight: bold; text-transform: uppercase; font-size: 9px; color: #000; }}
            .col-si-no {{ width: 20px; text-align: center; font-weight: bold; font-size: 10px; }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td style="width: 15%; text-align: center;"><img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="30"></td>
                <td style="text-align: center; font-weight: bold; font-size: 13px;">DECLARACIÓN JURADA DE SALUD</td>
            </tr>
        </table>

        <div class="section-title">AFILIACIÓN DEL TRABAJADOR</div>
        <table class="data-table">
            <tr>
                <td colspan="4"><span class="label">1. APELLIDOS Y NOMBRES</span><span class="value">{p.apellidos} {p.nombres}</span></td>
            </tr>
            <tr>
                <td style="width: 20%;"><span class="label">2. EDAD</span><span class="value">{f.edad if f else ''}</span></td>
                <td style="width: 20%;"><span class="label">3. SEXO</span><span class="value">{f.sexo if f else ''}</span></td>
                <td style="width: 30%;"><span class="label">4. FECHA NACIMIENTO</span><span class="value">{f.fecha_nacimiento if f else ''}</span></td>
                <td style="width: 30%;"><span class="label">5. LUGAR NACIMIENTO</span><span class="value">{f.lugar_nacimiento if f else ''}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">6. DOCUMENTO DE IDENTIDAD</span><span class="value">{p.ci}</span></td>
                <td colspan="2"><span class="label">7. ESTADO CIVIL</span><span class="value">{f.estado_civil if f else ''}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">8. DOMICILIO ACTUAL</span><span class="value">{f.domicilio if f else ''} # {f.n_casa if f else ''}</span></td>
                <td><span class="label">9. ZONA/BARRIO</span><span class="value">{f.zona_barrio if f else ''}</span></td>
                <td><span class="label">10. CIUDAD/PAÍS</span><span class="value">{f.ciudad if f else ''}, {f.pais if f else ''}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">11. TELÉFONO / CELULAR</span><span class="value">{f.telefono if f else ''}</span></td>
                <td colspan="2"><span class="label">12. PROFESIÓN U OFICIO</span><span class="value">{f.profesion_oficio if f else ''}</span></td>
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
                {"".join([f"<tr><td>{label}</td><td class='col-si-no'>{mark(getattr(a, f'p{i}', ''), 'SI') if a else ''}</td><td class='col-si-no'>{mark(getattr(a, f'p{i}', ''), 'NO') if a else ''}</td><td class='value'>{getattr(a, f'd{i}', '') if a else ''}</td></tr>" 
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
            </tbody>
        </table>
        <script>window.print();</script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
