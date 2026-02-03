from pydantic import BaseModel
from typing import List, Optional

#--- ESQUEMAS PARA PACIENTE ---
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

#--- ESQUEMAS PARA DECLARACIÓN JURADA ---
class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    
    # Sección 1: Afiliación
    edad: Optional[int] = None
    sexo: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    estado_civil: Optional[str] = None
    domicilio: Optional[str] = None
    telefono: Optional[str] = None
    profesion_oficio: Optional[str] = None

    # Sección 2: Antecedentes Patológicos
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
    otros_antecedentes: Optional[str] = None

    # Sección 3: Historia Laboral y Hábitos
    fuma: Optional[bool] = False
    fuma_detalle: Optional[str] = None
    bebe: Optional[bool] = False
    bebe_detalle: Optional[str] = None
    drogas: Optional[bool] = False
    drogas_detalle: Optional[str] = None
    bolo_coca: Optional[bool] = False
    bolo_coca_detalle: Optional[str] = None
    edad_inicio_laboral: Optional[int] = None
    empresa_actual: Optional[str] = None
    riesgos_expuestos: Optional[str] = None
    uso_epp: Optional[bool] = False
    epp_detalle: Optional[str] = None

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    class Config:
        from_attributes = True
