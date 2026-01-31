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
    
    # --- SECCIÓN 1: AFILIACIÓN ---
    edad: Optional[int] = 0
    sexo: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    lugar_nacimiento: Optional[str] = ""
    domicilio_av_calle: Optional[str] = ""
    domicilio_numero: Optional[str] = ""
    barrio: Optional[str] = ""
    ciudad: Optional[str] = ""
    pais: Optional[str] = ""
    telefono: Optional[str] = ""
    estado_civil: Optional[str] = ""
    profesion_labor: Optional[str] = ""

    # --- SECCIÓN 2: ANTECEDENTES DE SALUD ---
    vista: Optional[str] = "NO"
    auditivo: Optional[str] = "NO"
    respiratorios: Optional[str] = "NO"
    cardio: Optional[str] = "NO"
    digestivo: Optional[str] = "NO"
    sangre: Optional[str] = "NO"
    urinario: Optional[str] = "NO"
    nervioso: Optional[str] = "NO"
    psiquiatrico: Optional[str] = "NO"
    oseo: Optional[str] = "NO"
    metabolico: Optional[str] = "NO"
    reuma: Optional[str] = "NO"
    generales: Optional[str] = "NO"
    piel: Optional[str] = "NO"
    infecciones: Optional[str] = "NO"
    
    alergia_med: Optional[str] = ""
    alergia_ali: Optional[str] = ""

    # --- SECCIÓN 3.1: HÁBITOS ---
    h_alc_sn: Optional[str] = "NO"
    h_alc_cant: Optional[str] = ""
    h_alc_freq: Optional[str] = ""
    
    h_tab_sn: Optional[str] = "NO"
    h_tab_cant: Optional[str] = ""
    h_tab_freq: Optional[str] = ""
    
    h_coca_sn: Optional[str] = "NO"
    h_coca_cant: Optional[str] = ""
    h_coca_freq: Optional[str] = ""

    # --- SECCIÓN 3.2: HISTORIA LABORAL ---
    historia_laboral: Optional[str] = ""

    # --- SECCIÓN 3.3: LOS 17 RIESGOS ---
    r_ruido: Optional[str] = "NO"
    r_radiacion: Optional[str] = "NO"
    r_vibracion: Optional[str] = "NO"
    r_mecanicos: Optional[str] = "NO"
    r_temperatura: Optional[str] = "NO"
    r_polvo: Optional[str] = "NO"
    r_humos: Optional[str] = "NO"
    r_gases: Optional[str] = "NO"
    r_metales: Optional[str] = "NO"
    r_plomo: Optional[str] = "NO"
    r_repetitivos: Optional[str] = "NO"
    r_carga: Optional[str] = "NO"
    r_psicologico: Optional[str] = "NO"
    r_biologico: Optional[str] = "NO"
    r_altura: Optional[str] = "NO"
    r_confinados: Optional[str] = "NO"
    r_otros: Optional[str] = "NO"
    
    observaciones: Optional[str] = ""

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
