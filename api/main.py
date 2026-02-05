from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
from fpdf import FPDF
import io

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# Configuración de CORS para permitir conexión desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ONLINE", "proyecto": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS DE PACIENTES (Registro Inicial) ---

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- RUTAS DE DECLARACIÓN JURADA (P1, P2, P3) ---

@app.post("/filiacion/")
def save_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    # Esta ruta recibe los datos de declaracion_jurada_p1.html
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/antecedentes/")
def save_antecedentes(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    # Esta ruta recibe los datos de declaracion_jurada_p2.html
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/habitos/")
def save_habitos(data: schemas.HabitosCreate, db: Session = Depends(get_db)):
    # Esta ruta recibe los datos de declaracion_jurada_p3.html
    return crud.create_habitos(db=db, habitos=data)

# --- GENERADOR DE PDF ---

@app.get("/generar-pdf/{paciente_id}")
def generar_pdf_historial(paciente_id: int, db: Session = Depends(get_db)):
    try:
        historial = crud.get_historial_completo(db, paciente_id=paciente_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        p = historial["paciente"]
        f = historial.get("filiacion")
        p2 = historial.get("antecedentes")
        p3 = historial.get("habitos")

        pdf = FPDF()
        pdf.add_page()
        
        # ENCABEZADO
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "DECLARACION JURADA DE SALUD", ln=True, align="C")
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 5, "PROYECTO: HISTORIAL_CLINICO_NUBE", ln=True, align="C")
        pdf.ln(5)

        # 1. AFILIACION
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 1. AFILIACION DEL TRABAJADOR", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 7, f"Nombre Completo: {p.nombres} {p.apellidos}", border="B", ln=True)
        pdf.cell(60, 7, f"CI: {p.ci}", border="B")
        pdf.cell(60, 7, f"Edad: {f.edad if f else '---'}", border="B")
        pdf.cell(0, 7, f"Sexo: {f.sexo if f else '---'}", border="B", ln=True)
        pdf.cell(90, 7, f"Profesion: {f.profesion_oficio if f else '---'}", border="B")
        pdf.cell(0, 7, f"Ciudad: {f.ciudad if f else '---'}", border="B", ln=True)
        pdf.ln(5)

        # 2. ANTECEDENTES (Mapeo de los campos principales)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 2. ANTECEDENTES PATOLOGICOS", ln=True, fill=True)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(50, 6, "AREA", border=1, align="C")
        pdf.cell(15, 6, "SI/NO", border=1, align="C")
        pdf.cell(0, 6, "DETALLES", border=1, align="C", ln=True)
        
        pdf.set_font("Helvetica", "", 8)
        areas = [
            ("VISTA", p2.p1 if p2 else "NO", p2.d1 if p2 else ""),
            ("AUDITIVO", p2.p2 if p2 else "NO", p2.d2 if p2 else ""),
            ("RESPIRATORIOS", p2.p3 if p2 else "NO", p2.d3 if p2 else ""),
            ("CARDIO-VASCULARES", p2.p4 if p2 else "NO", p2.d4 if p2 else ""),
            ("SISTEMA NERVIOSO", p2.p9 if p2 else "NO", p2.d9 if p2 else ""),
            ("OSTEOMUSCULARES", p2.p11 if p2 else "NO", p2.d11 if p2 else ""),
        ]

        for area, valor, det in areas:
            pdf.cell(50, 6, area, border=1)
            pdf.cell(15, 6, valor, border=1, align="C")
            pdf.cell(0, 6, (str(det)[:75] + '...') if len(str(det)) > 75 else str(det), border=1, ln=True)
        
        pdf.ln(5)

        # 3. HABITOS
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 3. HABITOS Y RIESGOS EXPOSICION", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        if p3:
            pdf.cell(60, 7, f"Fuma: {p3.fuma}", border=1)
            pdf.cell(60, 7, f"Bebe: {p3.bebe}", border=1)
            pdf.cell(0, 7, f"Drogas: {p3.drogas}", border=1, ln=True)
        else:
            pdf.cell(0, 7, "Sin registros de habitos.", border=1, ln=True)

        # FIRMA
        pdf.ln(15)
        pdf.cell(0, 10, "__________________________", ln=True, align="C")
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(0, 5, f"FIRMA DEL TRABAJADOR: {p.nombres} {p.apellidos}", ln=True, align="C")

        # Generar salida en bytes para FastAPI
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return Response(
            content=pdf_output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Historial_{p.codigo_paciente}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
