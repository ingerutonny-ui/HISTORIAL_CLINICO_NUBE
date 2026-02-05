from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import io
from fpdf import FPDF

try:
    models.Base.metadata.create_all(bind=engine)
    print("Base de datos conectada y tablas verificadas.")
except Exception as e:
    print(f"Error crítico de conexión: {e}")

app = FastAPI(title="HISTORIAL_CLINICO_NUBE")

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
    return {"status": "ONLINE", "database": "CONNECTED"}

# --- RUTAS DE PACIENTES ---

@app.post("/pacientes/", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_paciente(db=db, paciente=paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    try:
        return db.query(models.Paciente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pacientes/{codigo}", response_model=schemas.Paciente)
def read_paciente_por_codigo(codigo: str, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente_by_codigo(db, codigo=codigo)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

# --- RUTA DE GENERACIÓN DE PDF CORREGIDA ---

@app.get("/generar-pdf/{paciente_id}")
def generar_pdf_historial(paciente_id: int, db: Session = Depends(get_db)):
    try:
        historial = crud.get_historial_completo(db, paciente_id=paciente_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        
        # Encabezado
        pdf.cell(0, 10, "DECLARACION JURADA DE SALUD", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 10, "PROYECTO: HISTORIAL_CLINICO_NUBE", ln=True, align="C")
        pdf.ln(5)

        # Sección 1: Datos Personales
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 1. AFILIACION DEL TRABAJADOR", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        
        p = historial["paciente"]
        d1 = historial.get("declaracion")
        
        pdf.cell(0, 7, f"Nombre Completo: {p.nombres} {p.apellidos}", ln=True)
        pdf.cell(90, 7, f"CI: {p.ci}", ln=0)
        pdf.cell(0, 7, f"Edad: {d1.edad if d1 else 'N/A'}", ln=True)
        pdf.cell(90, 7, f"Sexo: {d1.sexo if d1 else 'N/A'}", ln=0)
        pdf.cell(0, 7, f"Profesion: {d1.profesion_oficio if d1 else 'N/A'}", ln=True)
        pdf.ln(5)

        # Sección 2: Vista de Antecedentes
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 2. RESUMEN DE ANTECEDENTES", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 7, "El paciente declara haber sido informado sobre la importancia de la veracidad en sus antecedentes patologicos.")
        pdf.ln(5)

        # Firma
        pdf.ln(20)
        pdf.cell(0, 10, "__________________________", ln=True, align="C")
        pdf.cell(0, 5, "FIRMA DEL TRABAJADOR", ln=True, align="C")

        # Exportar PDF a Bytes
        pdf_bytes = pdf.output()
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Historial_{p.codigo_paciente}.pdf"}
        )
        
    except Exception as e:
        print(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
