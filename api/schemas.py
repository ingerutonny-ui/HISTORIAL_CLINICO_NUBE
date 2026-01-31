from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- ESQUEMAS PARA PACIENTE ---
class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    documento_identidad: str
    codigo_paciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA DECLARACIÓN JURADA ---
class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    
    # --- SECCIÓN 1: DATOS COMPLEMENTARIOS ---
    domicilio_av_calle: Optional[str] = None
    domicilio_numero: Optional[str] = None
    barrio: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    profesion_labor: Optional[str] = None
    telefono: Optional[str] = None
    estado_civil: Optional[str] = None

    # --- SECCIÓN 2: ANTECEDENTES PATOLÓGICOS ---
    vista: Optional[str] = None
    auditivo: Optional[str] = None
    respiratorios: Optional[str] = None
    cardiovasculares: Optional[str] = None
    estomago_intestino: Optional[str] = None
    sangre: Optional[str] = None
    genitourinario: Optional[str] = None
    sistema_nervioso: Optional[str] = None
    psiquiatricos_mentales: Optional[str] = None
    osteomusculares: Optional[str] = None
    endocrinos_metabolicos: Optional[str] = None
    reumatologicos: Optional[str] = None
    dermatologicos: Optional[str] = None
    generales_cancer_hernias: Optional[str] = None
    
    # ALERGIAS E INFECCIONES
    alergias_medicamentos: Optional[str] = None
    alergias_alimentos: Optional[str] = None
    infecciones_detalle: Optional[str] = None
    
    # --- SECCIÓN 3: PERSONALES, HÁBITOS Y LABORAL ---
    cirugias: Optional[str] = None
    accidentes_trabajo: Optional[str] = None
    accidentes_particulares: Optional[str] = None
    medicamentos_uso_actual: Optional[str] = None
    grupo_sanguineo: Optional[str] = None
    deportes: Optional[str] = None
    
    alcohol: Optional[str] = None
    tabaco: Optional[str] = None
    drogas: Optional[str] = None
    coca_bolo: Optional[str] = None
    
    edad_inicio_trabajo: Optional[int] = None
    historia_laboral_detalle: Optional[str] = None
    riesgos_expuestos: Optional[str] = None
    uso_epp: Optional[str] = None
    
    observaciones: Optional[str] = None

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
