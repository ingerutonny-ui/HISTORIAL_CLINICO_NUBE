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
    model_config = ConfigDict(from_attributes=True, extra='allow')

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: Optional[Any] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    domicilio: Optional[str] = None
    n_casa: Optional[str] = None
    zona_barrio: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    telefono: Optional[str] = None
    estado_civil: Optional[str] = None
    profesion_oficio: Optional[str] = None
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
    fuma_cantidad: Optional[str] = ""
    alcohol: Optional[str] = "NO"
    alcohol_frecuencia: Optional[str] = ""
    drogas: Optional[str] = "NO"
    drogas_tipo: Optional[str] = ""
    coca: Optional[str] = "NO"
    deporte: Optional[str] = "NO"
    deporte_detalle: Optional[str] = ""
    grupo_sanguineo: Optional[str] = ""
    historia_laboral: Optional[Any] = "[]"
    riesgos_expuestos: Optional[Any] = "[]"
    observaciones: Optional[str] = ""
    model_config = ConfigDict(extra='allow')
