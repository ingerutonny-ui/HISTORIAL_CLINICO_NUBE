from pydantic import BaseModel
from typing import List, Optional

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
    vista: Optional[str] = None
    auditivo: Optional[str] = None
    respiratorios: Optional[str] = None
    cardiovasculares: Optional[str] = None
    digestivos: Optional[str] = None
    genitourinario: Optional[str] = None
    sistema_nervioso: Optional[str] = None
    osteomusculares: Optional[str] = None
    endocrinos: Optional[str] = None
    dermatologicos: Optional[str] = None
    alergias_medicamentos: Optional[str] = None
    chagas: Optional[str] = None
    hepatitis: Optional[str] = None
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
    empresa_actual: Optional[str] = None
    ocupacion_actual: Optional[str] = None
    tiempo_trabajo: Optional[str] = None
    riesgos_expuestos: Optional[str] = None
    uso_epp: Optional[str] = None

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    class Config:
        from_attributes = True
