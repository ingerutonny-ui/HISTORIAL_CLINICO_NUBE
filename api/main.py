from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import json
from . import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/generar-pdf/{paciente_id}", response_class=HTMLResponse)
def generar_reporte(paciente_id: int, db: Session = Depends(get_db)):
    res = crud.get_historial_completo(db, paciente_id)
    p, f, a, h = res["paciente"], res["filiacion"], res["antecedentes"], res["habitos"]
    
    if not p: raise HTTPException(status_code=404)

    def get_v(obj, attr, default="---"):
        val = getattr(obj, attr, None)
        if val is None or str(val).strip() == "" or str(val).upper() == "NONE":
            return default
        return str(val).upper()

    def mark(obj, attr, target):
        val = getattr(obj, attr, None)
        return "X" if str(val).strip().upper() == target else ""

    # Sección II: Antecedentes (1-18)
    labels = ["VISTA", "AUDITIVO", "RESPIRATORIO", "CARDIO-VASCULARES", "ESTÓMAGO/HÍGADO", "SANGRE", "GENITO-URINARIO", "SISTEMA NERVIOSO", "PSIQUIÁTRICOS", "OSTEOMUSCULARES", "ENDOCRINOLÓGICOS", "REUMATOLÓGICOS", "GENERALES", "DERMATOLÓGICAS", "ALERGIA", "INFECCIONES", "CIRUGÍAS", "ACCIDENTES DE TRABAJO"]
    rows_p2 = "".join([f"<tr><td>{i+1}. {l}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','SI')}</td><td style='text-align:center;'>{mark(a,f'p{i+1}','NO')}</td><td>{get_v(a,f'd{i+1}')}</td></tr>" for i,l in enumerate(labels)])

    # Sección III: Historia Laboral
    filas_h = "<tr><td colspan='6' style='text-align:center;'>SIN REGISTROS</td></tr>"
    if h and h.historia_laboral:
        try:
            items = json.loads(h.historia_laboral)
            filas_h = "".join([f"<tr><td>{i.get('edad','-')}</td><td>{i.get('emp','-')}</td><td>{i.get('ocu','-')}</td><td>{i.get('tie','-')}</td><td>{i.get('rie','-')}</td><td>{i.get('epp','-')}</td></tr>" for i in items])
        except: pass

    html = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><style>
        @media print {{ .page-break {{ page-break-before: always; }} }}
        body {{ font-family: 'Arial Narrow', Arial; font-size: 10px; text-transform: uppercase; margin: 0; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
        td {{ border: 1px solid black; padding: 5px; }}
        .header {{ background: #d9e2f3; font-weight: bold; text-align: center; font-size: 11px; }}
        .title {{ text-align: center; font-size: 14px; font-weight: bold; margin-bottom: 20px; }}
    </style></head><body>
        <div class="title">DECLARACIÓN JURADA DE SALUD</div>
        <table>
            <tr><td colspan="4" class="header">I. AFILIACIÓN DEL TRABAJADOR</td></tr>
            <tr><td width="20%"><b>NOMBRES:</b></td><td colspan="3">{get_v(p,'apellidos')} {get_v(p,'nombres')}</td></tr>
            <tr><td><b>EDAD:</b></td><td>{get_v(f,'edad')} AÑOS</td><td width="20%"><b>SEXO:</b></td><td>{get_v(f,'sexo')}</td></tr>
            <tr><td><b>FECHA NAC.:</b></td><td>{get_v(f,'fecha_nacimiento')}</td><td><b>C.I.:</b></td><td>{get_v(p,'ci')}</td></tr>
            <tr><td><b>DOMICILIO:</b></td><td colspan="3">{get_v(f,'domicilio')} No. {get_v(f,'n_casa')}, {get_v(f,'zona_barrio')}</td></tr>
            <tr><td><b>CIUDAD/PAÍS:</b></td><td>{get_v(f,'ciudad')} / {get_v(f,'pais')}</td><td><b>TELÉFONO:</b></td><td>{get_v(f,'telefono')}</td></tr>
            <tr><td><b>PROFESIÓN:</b></td><td colspan="3">{get_v(f,'profesion_oficio')}</td></tr>
        </table>
        <table>
            <tr class="header"><td>II. ANTECEDENTES</td><td width="40px">SI</td><td width="40px">NO</td><td>DETALLES / OBSERVACIONES</td></tr>
            {rows_p2}
        </table>

        <div class="page-break"></div>
        <table>
            <tr class="header"><td colspan="4">CONTINUACIÓN ANTECEDENTES Y HABITOS</td></tr>
            <tr><td>19. ACCIDENTES PARTICULARES</td><td width="40px" style="text-align:center;">{mark(h,'accidentes_si_no','SI')}</td><td width="40px" style="text-align:center;">{mark(h,'accidentes_si_no','NO')}</td><td>{get_v(h,'accidentes_detalle')}</td></tr>
            <tr><td>20. MEDICAMENTOS</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','SI')}</td><td style="text-align:center;">{mark(h,'medicamentos_si_no','NO')}</td><td>{get_v(h,'medicamentos_detalle')}</td></tr>
            <tr><td>21. GRUPO SANGUÍNEO</td><td colspan="2"></td><td style="font-weight:bold; text-align:center;">{get_v(h,'grupo_sanguineo')}</td></tr>
            <tr><td>22. DEPORTES</td><td style="text-align:center;">{mark(h,'deportes_si_no','SI')}</td><td style="text-align:center;">{mark(h,'deportes_si_no','NO')}</td><td>{get_v(h,'deportes_detalle')}</td></tr>
        </table>
        <div class="header" style="border:1px solid black;">III. ANTECEDENTES OCUPACIONALES (HISTORIA LABORAL)</div>
        <table>
            <tr class="header" style="font-size:9px;"><td>EDAD</td><td>EMPRESA</td><td>OCUPACIÓN</td><td>TIEMPO</td><td>RIESGOS</td><td>EPP</td></tr>
            {filas_h}
        </table>
        <div class="header" style="border:1px solid black; margin-top:10px;">IV. RIESGOS EXPUESTOS DURANTE VIDA LABORAL</div>
        <div style="border:1px solid black; padding:15px; min-height:60px; font-size:11px;">{get_v(h, 'riesgos_vida_laboral')}</div>
        <br><br>
        <div style="display:flex; justify-content: space-around; margin-top:50px;">
            <div style="text-align:center; border-top:1px solid black; width:200px;">FIRMA DEL TRABAJADOR</div>
            <div style="text-align:center; border-top:1px solid black; width:200px;">HUELLA DIGITAL</div>
        </div>
        <script>window.print();</script>
    </body></html>
    """
    return HTMLResponse(content=html)
