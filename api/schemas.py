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
    n_casa: str
    zona: str
    ciudad: str
    pais: str
    telefono: str
    estado_civil: str
    profesion: str

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: str
    vista_obs: str
    auditivo: str
    auditivo_obs: str
    respiratorio: str
    respiratorio_obs: str
    cardiovasculares: str
    cardiovasculares_obs: str
    digestivos: str
    digestivos_obs: str
    sangre: str
    sangre_obs: str
    genitourinario: str
    genitourinario_obs: str
    sistema_nervioso: str
    sistema_nervioso_obs: str
    psiquiatricos: str
    psiquiatricos_obs: str
    osteomusculares: str
    osteomusculares_obs: str
    endocrino: str
    endocrino_obs: str
    alergias: str
    alergias_obs: str
    cirugias: str
    cirugias_obs: str
    accidentes_trabajo: str
    accidentes_trabajo_obs: str
    accidentes_pers: str
    accidentes_pers_obs: str
    medicamentos: str
    medicamentos_obs: str
    infecciosas: str
    infecciosas_obs: str
    ap_urinario: str
    ap_urinario_obs: str
    linfatico: str
    linfatico_obs: str
    reumatologicos: str
    reumatologicos_obs: str
    otros: str
    otros_obs: str
    generales: str
    generales_obs: str

class HabitosP3Create(BaseModel):
    paciente_id: int
    fuma: str
    bebe_alcohol: str
    deporte: str
    observaciones: str
