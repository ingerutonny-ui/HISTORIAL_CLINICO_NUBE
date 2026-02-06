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
def generar_reporte_completo(paciente_id: int, db: Session = Depends(get_db)):
    data = crud.get_historial_completo(db, paciente_id)
    if not data["paciente"]:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p = data["paciente"]
    f = data["filiacion"]
    a = data["antecedentes"]
    h = data["habitos"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte Oficial - {p.codigo_paciente}</title>
        <style>
            @page {{ size: letter; margin: 15mm; }}
            body {{ font-family: 'Helvetica', Arial, sans-serif; font-size: 10px; line-height: 1.3; color: #1a1a1a; }}
            .header-table {{ width: 100%; border-bottom: 2px solid #24a174; margin-bottom: 15px; padding-bottom: 5px; }}
            .logo-text {{ font-size: 24px; font-weight: 900; color: #24a174; letter-spacing: -1px; }}
            .title-box {{ text-align: center; }}
            .title-main {{ font-size: 14px; font-weight: bold; text-transform: uppercase; margin: 0; }}
            .title-sub {{ font-size: 9px; color: #666; font-weight: normal; margin: 2px 0; }}
            
            .section-header {{ background-color: #f8fafc; border: 1px solid #e2e8f0; font-weight: bold; padding: 5px 10px; margin-top: 15px; text-transform: uppercase; color: #1e293b; border-left: 4px solid #24a174; }}
            
            .data-table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
            .data-table td {{ border: 1px solid #e2e8f0; padding: 6px; vertical-align: top; }}
            .label {{ font-weight: bold; font-size: 8px; color: #64748b; text-transform: uppercase; display: block; margin-bottom: 2px; }}
            .value {{ font-size: 10px; font-weight: 600; color: #0f172a; }}
            
            .medical-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 1px solid #e2e8f0; }}
            .medical-item {{ padding: 6px; border: 0.5px solid #f1f5f9; }}
            
            .declaration-footer {{ margin-top: 30px; padding: 15px; background: #fdfdfd; border: 1px dashed #cbd5e1; font-size: 9px; text-align: justify; line-height: 1.5; }}
            .signature-area {{ margin-top: 60px; width: 100%; }}
            .sig-line {{ border-top: 1px solid #000; width: 200px; margin: 0 auto; text-align: center; padding-top: 5px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td width="20%"><span class="logo-text">ohs</span></td>
                <td class="title-box">
                    <p class="title-main">Declaración Jurada de Salud</p>
                    <p class="title-sub">TRABAJO SANO, SEGURO Y PRODUCTIVO</p>
                </td>
                <td width="20%" style="text-align: right;">
                    <span class="label">Código Registro</span>
                    <span class="value">{p.codigo_paciente}</span>
                </td>
            </tr>
        </table>

        <div class="section-header">1. Afiliación del Trabajador</div>
        <table class="data-table">
            <tr>
                <td colspan="2"><span class="label">Apellidos y Nombres</span><span class="value">{p.nombres} {p.apellidos}</span></td>
                <td><span class="label">Edad</span><span class="value">{f.edad if f else '---'} Años</span></td>
                <td><span class="label">Sexo</span><span class="value">{f.sexo if f else '---'}</span></td>
            </tr>
            <tr>
                <td><span class="label">C.I.</span><span class="value">{p.ci}</span></td>
                <td><span class="label">Fecha Nacimiento</span><span class="value">{f.fecha_nacimiento if f else '---'}</span></td>
                <td colspan="2"><span class="label">Domicilio</span><span class="value">{f.domicilio if f else '---'} #{f.n_casa if f else 'S/N'}</span></td>
            </tr>
            <tr>
                <td><span class="label">Ciudad/País</span><span class="value">{f.ciudad if f else '---'} / {f.pais if f else '---'}</span></td>
                <td><span class="label">Teléfono</span><span class="value">{f.telefono if f else '---'}</span></td>
                <td colspan="2"><span class="label">Estado Civil / Profesión</span><span class="value">{f.estado_civil if f else '---'} / {f.profesion_oficio if f else '---'}</span></td>
            </tr>
        </table>

        <div class="section-header">2. Antecedentes Patológicos (Resumen por Sistemas)</div>
        <table class="data-table">
            <tr>
                <td width="50%"><span class="label">Vista / Oftalmológico</span><span class="value">{a.p1 if a else 'NO'} - {a.d1 if a else ''}</span></td>
                <td width="50%"><span class="label">Cardio-Vascuales (Presión)</span><span class="value">{a.p4 if a else 'NO'} - {a.d4 if a else ''}</span></td>
            </tr>
            <tr>
                <td><span class="label">Auditivo</span><span class="value">{a.p2 if a else 'NO'} - {a.d2 if a else ''}</span></td>
                <td><span class="label">Respiratorios</span><span class="value">{a.p3 if a else 'NO'} - {a.d3 if a else ''}</span></td>
            </tr>
            <tr>
                <td><span class="label">Gastrointestinales</span><span class="value">{a.p5 if a else 'NO'} - {a.d5 if a else ''}</span></td>
                <td><span class="label">Diabetes / Endocrino</span><span class="value">{a.p1 if a else 'NO'}</span></td>
            </tr>
        </table>

        <div class="section-header">3. Hábitos y Factores de Riesgo</div>
        <table class="data-table">
            <tr>
                <td><span class="label">Consumo Alcohol</span><span class="value">{h.h2 if h else 'NO'} ({h.r2 if h else 'N/A'})</span></td>
                <td><span class="label">Consumo Tabaco</span><span class="value">{h.h1 if h else 'NO'} ({h.r1 if h else 'N/A'})</span></td>
                <td><span class="label">Grupo Sanguíneo</span><span class="value">{h.r10 if h else 'S/D'}</span></td>
            </tr>
            <tr>
                <td colspan="3"><span class="label">Actividad Física / Deportes</span><span class="value">{h.h5 if h else 'NO'} - {h.r5 if h else 'Ninguno'}</span></td>
            </tr>
        </table>

        <div class="declaration-footer">
            Por medio de la presente, yo <strong>{p.nombres} {p.apellidos}</strong>, declaro bajo juramento que toda la información médico-biográfica proporcionada es verdadera y no he omitido datos sobre mi estado de salud actual o pasado. Entiendo que cualquier falsedad invalida este documento según normativa vigente del Ministerio de Salud.
        </div>

        <div class="signature-area">
            <div class="sig-line">
                Firma del Trabajador/Paciente<br>
                <span style="font-size: 8px;">C.I.: {p.ci}</span>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
