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

# --- RUTAS DE PACIENTES (EXTENDIDAS) ---

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

@app.put("/pacientes/{codigo}", response_model=schemas.Paciente)
def update_paciente(codigo: str, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, codigo=codigo, datos_actualizados=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="No se pudo actualizar: Paciente no encontrado")
    return db_paciente

@app.delete("/pacientes/{codigo}")
def delete_paciente(codigo: str, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, codigo=codigo)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: Paciente no encontrado")
    return {"message": f"Paciente {codigo} eliminado exitosamente"}

# --- RUTAS DE DECLARACIONES (GUARDADO) ---

@app.post("/declaraciones/p1/", response_model=schemas.DeclaracionJurada)
def save_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_declaracion_p1(db=db, declaracion=declaracion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p2/", response_model=schemas.AntecedentesP2)
def save_p2(antecedentes: schemas.AntecedentesP2Create, db: Session = Depends(get_db)):
    try:
        return crud.create_antecedentes_p2(db=db, antecedentes=antecedentes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/declaraciones/p3/", response_model=schemas.HabitosRiesgosP3)
def save_p3(habitos: schemas.HabitosRiesgosP3Create, db: Session = Depends(get_db)):
    try:
        return crud.create_habitos_p3(db=db, habitos=habitos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RUTA DE CONSULTA INTEGRAL Y GENERACIÓN DE PDF ---

@app.get("/historial-completo/{paciente_id}", response_model=schemas.HistorialCompleto)
def get_historial_completo(paciente_id: int, db: Session = Depends(get_db)):
    historial = crud.get_historial_completo(db, paciente_id=paciente_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial

@app.get("/generar-pdf/{paciente_id}")
def generar_pdf_historial(paciente_id: int, db: Session = Depends(get_db)):
    historial = crud.get_historial_completo(db, paciente_id=paciente_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Encabezado
    pdf.cell(0, 10, "DECLARACION JURADA DE SALUD", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, "PROYECTO: HISTORIAL_CLINICO_NUBE", ln=True, align="C")
    pdf.ln(5)

    # Datos Personales (P1)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 8, "1. AFILIACION DEL TRABAJADOR", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    p = historial["paciente"]
    d1 = historial["declaracion"]
    
    pdf.cell(0, 7, f"Nombre Completo: {p.nombres} {p.apellidos}", ln=True)
    pdf.cell(90, 7, f"CI: {p.ci}", ln=0)
    pdf.cell(0, 7, f"Edad: {d1.edad if d1 else 'N/A'}", ln=True)
    pdf.cell(90, 7, f"Sexo: {d1.sexo if d1 else 'N/A'}", ln=0)
    pdf.cell(0, 7, f"Profesion: {d1.profesion_oficio if d1 else 'N/A'}", ln=True)
    pdf.ln(5)

    # Antecedentes (P2)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 8, "2. ANTECEDENTES PATOLOGICOS", ln=True, fill=True)
    # Aquí se pueden iterar los campos p1..p22 si existen datos
    pdf.cell(0, 7, "Revisar registro digital para detalle de indicadores p1-p22.", ln=True)
    pdf.ln(5)

    # Hábitos (P3)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 8, "3. HABITOS Y RIESGOS", ln=True, fill=True)
    h3 = historial["habitos_riesgos"]
    if h3:
        pdf.cell(0, 7, f"Fuma: {h3.fuma} ({h3.fuma_det})", ln=True)
        pdf.cell(0, 7, f"Bebe: {h3.bebe} ({h3.bebe_det})", ln=True)
        pdf.cell(0, 7, f"Riesgos Fisicos: {h3.r_fisico}", ln=True)

    # Generar salida
    pdf_output = io.BytesIO()
    pdf_str = pdf.output(dest='S')
    pdf_output.write(pdf_str)
    pdf_output.seek(0)

    return Response(
        content=pdf_output.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=Historial_{p.codigo_paciente}.pdf"}
    )
