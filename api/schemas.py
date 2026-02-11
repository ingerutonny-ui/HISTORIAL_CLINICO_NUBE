from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str
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
    model_config = ConfigDict(from_attributes=True, extra='allow')
