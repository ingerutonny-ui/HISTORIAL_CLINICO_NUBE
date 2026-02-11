from pydantic import BaseModel, ConfigDict
from typing import Optional

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str
    model_config = ConfigDict(from_attributes=True)

class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    edad: Optional[str] = None
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
    model_config = ConfigDict(from_attributes=True, extra='allow')

class AntecedentesP2Base(BaseModel):
    paciente_id: int
    model_config = ConfigDict(from_attributes=True, extra='allow')

class HabitosRiesgosP3Base(BaseModel):
    paciente_id: int
    model_config = ConfigDict(from_attributes=True, extra='allow')
