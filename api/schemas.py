from pydantic import BaseModel, ConfigDict
from typing import Optional

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
    model_config = ConfigDict(extra='allow')

class AntecedentesCreate(BaseModel):
    paciente_id: int
    model_config = ConfigDict(extra='allow')

class HabitosP3Create(BaseModel):
    paciente_id: int
    model_config = ConfigDict(extra='allow')
