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

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def read_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

# --- GENERADOR DE PDF PROFESIONAL ---

class PDF_Protocolo(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "DECLARACION JURADA DE SALUD", ln=True, align="C")
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 5, "SISTEMA DE GESTION CLINICA - HISTORIAL_CLINICO_NUBE", ln=True, align="C")
        self.ln(5)

@app.get("/generar-pdf/{paciente_id}")
def generar_pdf_historial(paciente_id: int, db: Session = Depends(get_db)):
    try:
        historial = crud.get_historial_completo(db, paciente_id=paciente_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")

        p = historial["paciente"]
        d1 = historial.get("declaracion")
        p2 = historial.get("antecedentes")
        p3 = historial.get("habitos_riesgos")

        pdf = PDF_Protocolo()
        pdf.add_page()
        
        # 1. AFILIACION
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 1. AFILIACION DEL TRABAJADOR", ln=True, fill=True)
        
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 7, f"Nombre Completo: {p.nombres} {p.apellidos}", border="B", ln=True)
        pdf.cell(60, 7, f"CI: {p.ci}", border="B")
        pdf.cell(60, 7, f"Edad: {d1.edad if d1 else '---'}", border="B")
        pdf.cell(0, 7, f"Sexo: {d1.sexo if d1 else '---'}", border="B", ln=True)
        pdf.cell(90, 7, f"Profesion/Labor: {d1.profesion_oficio if d1 else '---'}", border="B")
        pdf.cell(0, 7, f"Ciudad: {d1.ciudad if d1 else '---'}", border="B", ln=True)
        pdf.ln(4)

        # 2. ANTECEDENTES (TABLA SI/NO)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 2. ANTECEDENTES PATOLOGICOS", ln=True, fill=True)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(50, 6, "AREA", border=1, align="C")
        pdf.cell(15, 6, "SI/NO", border=1, align="C")
        pdf.cell(0, 6, "DETALLES / OBSERVACIONES", border=1, align="C", ln=True)
        
        pdf.set_font("Helvetica", "", 8)
        areas = [
            ("VISTA", p2.p1 if p2 else "NO", p2.d1 if p2 else ""),
            ("AUDITIVO", p2.p2 if p2 else "NO", p2.d2 if p2 else ""),
            ("RESPIRATORIOS", p2.p3 if p2 else "NO", p2.d3 if p2 else ""),
            ("CARDIO-VASCULARES", p2.p4 if p2 else "NO", p2.d4 if p2 else ""),
            ("SISTEMA NERVIOSO", p2.p9 if p2 else "NO", p2.d9 if p2 else ""),
        ]

        for area, valor, det in areas:
            pdf.cell(50, 6, area, border=1)
            pdf.cell(15, 6, valor, border=1, align="C")
            pdf.cell(0, 6, str(det)[:70], border=1, ln=True)
        
        pdf.ln(4)

        # 3. HABITOS Y RIESGOS
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, " 3. HABITOS Y RIESGOS EXPOSICION", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 9)
        
        if p3:
            pdf.cell(60, 7, f"Fuma: {p3.fuma} ({p3.fuma_det})", border=1)
            pdf.cell(60, 7, f"Bebe: {p3.bebe} ({p3.bebe_det})", border=1)
            pdf.cell(0, 7, f"Drogas: {p3.drogas}", border=1, ln=True)
            
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(0, 6, "RIESGOS DETECTADOS EN VIDA LABORAL:", ln=True)
            pdf.set_font("Helvetica", "", 8)
            pdf.multi_cell(0, 5, f"FISICOS: {p3.r_fisico} | QUIMICOS: {p3.r_quimico} | ERGONOMICOS: {p3.r_ergonomico}", border=1)
        else:
            pdf.cell(0, 7, "No se encontraron registros de habitos y riesgos.", ln=True)

        # FIRMA FINAL
        pdf.ln(15)
        pdf.set_font("Helvetica", "I", 7)
        pdf.multi_cell(0, 4, "Declaro que toda la informacion proporcionada es verdadera y autorizo su uso para fines medicos legales.", align="C")
        pdf.ln(10)
        pdf.cell(0, 10, "__________________________", ln=True, align="C")
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(0, 5, f"FIRMA: {p.nombres} {p.apellidos}", ln=True, align="C")
        pdf.cell(0, 5, f"CI: {p.ci}", ln=True, align="C")

        pdf_bytes = pdf.output()
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Declaracion_{p.codigo_paciente}.pdf"}
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
