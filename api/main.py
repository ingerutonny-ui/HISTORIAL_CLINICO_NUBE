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

# CONFIGURACIÓN CORS PARA ELIMINAR EL ERROR DE RED DE GITHUB
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
    if not data:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p = data["paciente"]
    f = data.get("filiacion")
    
    # Construcción del HTML con el diseño de tus capturas
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 10mm; }}
            body {{ font-family: Arial, sans-serif; font-size: 9px; color: #333; }}
            .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid black; margin-bottom: 5px; }}
            .header-table td {{ border: 1px solid black; padding: 5px; text-align: center; }}
            .title {{ font-weight: bold; font-size: 14px; background-color: #f0f0f0; }}
            .section-title {{ background-color: #d9e2f3; font-weight: bold; text-transform: uppercase; padding: 3px; border: 1px solid black; }}
            .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
            .data-table td, .data-table th {{ border: 1px solid black; padding: 4px; }}
            .label {{ font-weight: bold; font-size: 8px; color: #555; }}
            .value {{ font-weight: bold; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td style="width: 20%;"><img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="40"></td>
                <td class="title">DECLARACIÓN JURADA DE SALUD</td>
            </tr>
        </table>

        <div class="section-title">AFILIACIÓN DEL TRABAJADOR</div>
        <table class="data-table">
            <tr>
                <td colspan="4"><span class="label">APELLIDOS Y NOMBRES:</span><br><span class="value">{p.apellidos} {p.nombres}</span></td>
            </tr>
            <tr>
                <td><span class="label">EDAD:</span><br><span class="value">{f.edad if f else '-'}</span></td>
                <td><span class="label">SEXO:</span><br><span class="value">{f.sexo if f else '-'}</span></td>
                <td colspan="2"><span class="label">DOCUMENTO DE IDENTIDAD:</span><br><span class="value">{p.ci}</span></td>
            </tr>
            <tr>
                <td><span class="label">FECHA NACIMIENTO:</span><br><span class="value">{f.fecha_nacimiento if f else '-'}</span></td>
                <td><span class="label">LUGAR:</span><br><span class="value">{f.lugar_nacimiento if f else '-'}</span></td>
                <td><span class="label">ESTADO CIVIL:</span><br><span class="value">{f.estado_civil if f else '-'}</span></td>
                <td><span class="label">PROFESIÓN:</span><br><span class="value">{f.profesion_oficio if f else '-'}</span></td>
            </tr>
            <tr>
                <td colspan="2"><span class="label">DOMICILIO:</span><br><span class="value">{f.domicilio if f else '-'} # {f.n_casa if f else '-'}</span></td>
                <td><span class="label">CIUDAD:</span><br><span class="value">{f.ciudad if f else '-'}</span></td>
                <td><span class="label">TELÉFONO:</span><br><span class="value">{f.telefono if f else '-'}</span></td>
            </tr>
        </table>

        <div style="text-align: center; font-size: 7px; margin-top: 20px;">
            <p>Por medio de este documento médico legal declaro que es verdad toda la información proporcionada.</p>
            <br><br>
            ________________________________<br>
            FIRMA DEL TRABAJADOR
        </div>
        
        <script>window.print();</script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
