from pydantic import BaseModel
from typing import Optional

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    class Config:
        from_attributes = True

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: Optional[str] = ""
    sexo: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    lugar_nacimiento: Optional[str] = ""
    domicilio: Optional[str] = ""
    n_casa: Optional[str] = ""
    zona: Optional[str] = ""
    ciudad: Optional[str] = ""
    pais: Optional[str] = ""
    telefono: Optional[str] = ""
    estado_civil: Optional[str] = ""
    profesion: Optional[str] = ""

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: Optional[str] = "NO"
    vista_obs: Optional[str] = ""
    auditivo: Optional[str] = "NO"
    auditivo_obs: Optional[str] = ""
    respiratorio: Optional[str] = "NO"
    respiratorio_obs: Optional[str] = ""
    cardiovasculares: Optional[str] = "NO"
    cardiovasculares_obs: Optional[str] = ""
    digestivos: Optional[str] = "NO"
    digestivos_obs: Optional[str] = ""
    sangre: Optional[str] = "NO"
    sangre_obs: Optional[str] = ""
    genitourinario: Optional[str] = "NO"
    genitourinario_obs: Optional[str] = ""
    sistema_nervioso: Optional[str] = "NO"
    sistema_nervioso_obs: Optional[str] = ""
    psiquiatricos: Optional[str] = "NO"
    psiquiatricos_obs: Optional[str] = ""
    osteomusculares: Optional[str] = "NO"
    osteomusculares_obs: Optional[str] = ""
    endocrino: Optional[str] = "NO"
    endocrino_obs: Optional[str] = ""
    alergias: Optional[str] = "NO"
    alergias_obs: Optional[str] = ""
    cirugias: Optional[str] = "NO"
    cirugias_obs: Optional[str] = ""
    accidentes_trabajo: Optional[str] = "NO"
    accidentes_trabajo_obs: Optional[str] = ""
    accidentes_pers: Optional[str] = "NO"
    accidentes_pers_obs: Optional[str] = ""
    medicamentos: Optional[str] = "NO"
    medicamentos_obs: Optional[str] = ""
    infecciosas: Optional[str] = "NO"
    infecciosas_obs: Optional[str] = ""
    ap_urinario: Optional[str] = "NO"
    ap_urinario_obs: Optional[str] = ""
    linfatico: Optional[str] = "NO"
    linfatico_obs: Optional[str] = ""
    reumatologicos: Optional[str] = "NO"
    reumatologicos_obs: Optional[str] = ""
    otros: Optional[str] = "NO"
    otros_obs: Optional[str] = ""
    generales: Optional[str] = "NO"
    generales_obs: Optional[str] = ""

class HabitosP3Create(BaseModel):
    paciente_id: int
    fuma: Optional[str] = "NO"
    bebe_alcohol: Optional[str] = "NO"
    deporte: Optional[str] = "NO"
    observaciones: Optional[str] = ""
