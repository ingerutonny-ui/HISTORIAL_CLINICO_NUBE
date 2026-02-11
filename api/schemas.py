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
    sexo: Optional[Any] = None
    fecha_nacimiento: Optional[Any] = None
    lugar_nacimiento: Optional[Any] = None
    domicilio: Optional[Any] = None
    n_casa: Optional[Any] = None
    zona_barrio: Optional[Any] = None
    ciudad: Optional[Any] = None
    pais: Optional[Any] = None
    telefono: Optional[Any] = None
    estado_civil: Optional[Any] = None
    profesion_oficio: Optional[Any] = None
    model_config = ConfigDict(extra='allow')

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: Optional[Any] = "NORMAL"
    auditivo: Optional[Any] = "NORMAL"
    respiratorio: Optional[Any] = "NORMAL"
    cardio: Optional[Any] = "NORMAL"
    digestivos: Optional[Any] = "NORMAL"
    sangre: Optional[Any] = "NORMAL"
    genitourinario: Optional[Any] = "NORMAL"
    sistema_nervioso: Optional[Any] = "NORMAL"
    psiquiatricos: Optional[Any] = "NORMAL"
    osteomusculares: Optional[Any] = "NORMAL"
    reumatologicos: Optional[Any] = "NORMAL"
    dermatologicas: Optional[Any] = "NORMAL"
    alergias: Optional[Any] = "NORMAL"
    cirugias: Optional[Any] = "NORMAL"
    infecciones: Optional[Any] = "NORMAL"
    acc_personales: Optional[Any] = "NORMAL"
    acc_trabajo: Optional[Any] = "NORMAL"
    medicamentos: Optional[Any] = "NORMAL"
    endocrino: Optional[Any] = "NORMAL"
    familiares: Optional[Any] = "NORMAL"
    otros_especificos: Optional[Any] = "NORMAL"
    generales: Optional[Any] = "NORMAL"
    model_config = ConfigDict(extra='allow')

class HabitosP3Create(BaseModel):
    paciente_id: int
    fuma: Optional[Any] = "NO"
    fuma_cantidad: Optional[Any] = ""
    alcohol: Optional[Any] = "NO"
    alcohol_frecuencia: Optional[Any] = ""
    drogas: Optional[Any] = "NO"
    drogas_tipo: Optional[Any] = ""
    coca: Optional[Any] = "NO"
    deporte: Optional[Any] = "NO"
    deporte_detalle: Optional[Any] = ""
    grupo_sanguineo: Optional[Any] = ""
    historia_laboral: Optional[Any] = "[]"
    riesgos_expuestos: Optional[Any] = "[]"
    observaciones: Optional[Any] = ""
    model_config = ConfigDict(extra='allow')
