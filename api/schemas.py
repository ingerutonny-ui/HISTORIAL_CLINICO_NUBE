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
    edad: str
    sexo: str
    fecha_nacimiento: str
    lugar_nacimiento: str
    domicilio: str
    n_casa: Optional[str] = ""
    zona: Optional[str] = ""
    ciudad: str
    pais: str
    telefono: Optional[str] = ""
    estado_civil: str
    profesion: Optional[str] = ""

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: str
    vista_obs: Optional[str] = ""
    auditivo: str
    auditivo_obs: Optional[str] = ""
    respiratorio: str
    respiratorio_obs: Optional[str] = ""
    cardiovasculares: str
    cardiovasculares_obs: Optional[str] = ""
    digestivos: str
    digestivos_obs: Optional[str] = ""
    sangre: str
    sangre_obs: Optional[str] = ""
    genitourinario: str
    genitourinario_obs: Optional[str] = ""
    sistema_nervioso: str
    sistema_nervioso_obs: Optional[str] = ""
    psiquiatricos: str
    psiquiatricos_obs: Optional[str] = ""
    osteomusculares: str
    osteomusculares_obs: Optional[str] = ""
    endocrino: str
    endocrino_obs: Optional[str] = ""
    alergias: str
    alergias_obs: Optional[str] = ""
    cirugias: str
    cirugias_obs: Optional[str] = ""
    accidentes_trabajo: str
    accidentes_trabajo_obs: Optional[str] = ""
    accidentes_pers: str
    accidentes_pers_obs: Optional[str] = ""
    medicamentos: str
    medicamentos_obs: Optional[str] = ""
    infecciosas: str
    infecciosas_obs: Optional[str] = ""
    ap_urinario: Optional[str] = "NO"
    ap_urinario_obs: Optional[str] = ""
    linfatico: Optional[str] = "NO"
    linfatico_obs: Optional[str] = ""
    reumatologicos: str
    reumatologicos_obs: Optional[str] = ""
    otros: Optional[str] = "NO"
    otros_obs: Optional[str] = ""
    generales: str
    generales_obs: Optional[str] = ""

class HabitosP3Create(BaseModel):
    paciente_id: int
    fuma: str
    bebe_alcohol: str
    deporte: str
    observaciones: Optional[str] = ""
