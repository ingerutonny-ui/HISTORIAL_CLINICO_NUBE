from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str
    model_config = ConfigDict(extra='allow')

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: Any = ""
    sexo: Optional[str] = ""
    fecha_nacimiento: Optional[str] = ""
    lugar_nacimiento: Optional[str] = ""
    domicilio: Optional[str] = ""
    n_casa: Optional[str] = ""
    zona_barrio: Optional[str] = ""
    ciudad: Optional[str] = ""
    pais: Optional[str] = ""
    telefono: Optional[str] = ""
    estado_civil: Optional[str] = ""
    profesion_oficio: Optional[str] = ""
    model_config = ConfigDict(extra='allow')

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: Optional[str] = "NORMAL"
    auditivo: Optional[str] = "NORMAL"
    respiratorio: Optional[str] = "NORMAL"
    cardio: Optional[str] = "NORMAL"
    digestivos: Optional[str] = "NORMAL"
    sangre: Optional[str] = "NORMAL"
    genitourinario: Optional[str] = "NORMAL"
    sistema_nervioso: Optional[str] = "NORMAL"
    psiquiatricos: Optional[str] = "NORMAL"
    osteomusculares: Optional[str] = "NORMAL"
    reumatologicos: Optional[str] = "NORMAL"
    dermatologicas: Optional[str] = "NORMAL"
    alergias: Optional[str] = "NORMAL"
    cirugias: Optional[str] = "NORMAL"
    infecciones: Optional[str] = "NORMAL"
    acc_personales: Optional[str] = "NORMAL"
    acc_trabajo: Optional[str] = "NORMAL"
    medicamentos: Optional[str] = "NORMAL"
    endocrino: Optional[str] = "NORMAL"
    familiares: Optional[str] = "NORMAL"
    otros_especificos: Optional[str] = "NORMAL"
    generales: Optional[str] = "NORMAL"
    model_config = ConfigDict(extra='allow')

class HabitosP3Create(BaseModel):
    paciente_id: int
    fuma: Optional[str] = "NO"
    bebe_alcohol: Optional[str] = "NO"
    deporte: Optional[str] = "NINGUNO"
    observaciones: Optional[str] = "SIN OBSERVACIONES"
    model_config = ConfigDict(extra='allow')
