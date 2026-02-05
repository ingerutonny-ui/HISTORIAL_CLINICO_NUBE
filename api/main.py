from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
from fpdf import FPDF
import io

# Inicialización de base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

# Configuración CORS
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

@app.get("/")
def read_root():
    return {"status": "ONLINE", "proyecto": "HISTORIAL_CLINICO_NUBE"}

# --- RUTAS DE PACIENTES ---
@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- RUTAS DE DECLARACIÓN JURADA (P1, P2, P3) ---
@app.post("/filiacion/")
def save_filiacion(data: schemas.FiliacionCreate, db: Session = Depends(get_db)):
    return crud.create_filiacion(db=db, filiacion=data)

@app.post("/antecedentes/")
def save_antecedentes(data: schemas.AntecedentesCreate, db: Session = Depends(get_db)):
    return crud.create_antecedentes(db=db, antecedentes=data)

@app.post("/habitos/")
def save_habitos(data: schemas.HabitosCreate, db: Session = Depends(get_db)):
    return crud.create_habitos(db=db, habitos=data)

# --- GENERADOR DE PDF ---
@app.get("/generar-pdf/{paciente_id}")
def generar_pdf_historial(paciente_id: int, db: Session = Depends(get_db)):
    try:
        historial = crud.get_historial_completo(db, paciente_id=paciente_id)
        if not historial or not historial["paciente"]:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        p = historial["paciente"]
        f = historial.get("filiacion")
        p2 = historial.get("antecedentes")
        p3 = historial.get("habitos")

        pdf = FPDF()
        pdf.add_page()
        
        # Estilo del documento
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "HISTORIAL CLINICO - DECLARACION JURADA", ln=True, align="C")
        pdf.ln(5)

        # Sección 1: Datos Personales
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, " 1. DATOS DE FILIACION", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, f"Nombre: {p.nombres} {p.apellidos}", border="B", ln=True)
        pdf.cell(90, 8, f"CI: {p.ci}", border="B")
        pdf.cell(0, 8, f"Codigo: {p.codigo_paciente}", border="B", ln=True)
        
        if f:
            pdf.cell(45, 8, f"Edad: {f.edad}", border="B")
            pdf.cell(45, 8, f"Sexo: {f.sexo}", border="B")
            pdf.cell(0, 8, f"Estado Civil: {f.estado_civil}", border="B", ln=True)
            pdf.cell(0, 8, f"Profesion: {f.profesion_oficio}", border="B", ln=True)

        # Sección 2: Antecedentes
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, " 2. ANTECEDENTES PATOLOGICOS", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        if p2:
            pdf.cell(0, 7, f"Cirugias: {p2.cirugias}", border="B", ln=True)
            pdf.cell(0, 7, f"Accidentes: {p2.accidentes}", border="B", ln=True)
        else:
            pdf.cell(0, 7, "Sin registros de antecedentes.", ln=True)

        # Sección 3: Habitos
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, " 3. HABITOS", ln=True, fill=True)
        if p3:
            pdf.cell(45, 8, f"Fuma: {p3.fuma}", border=1)
            pdf.cell(45, 8, f"Bebe: {p3.bebe}", border=1)
            pdf.cell(45, 8, f"Drogas: {p3.drogas}", border=1)
            pdf.cell(0, 8, f"Sangre: {p3.grupo_sanguineo}", border=1, ln=True)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        return Response(
            content=pdf_output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=HC_{p.codigo_paciente}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
