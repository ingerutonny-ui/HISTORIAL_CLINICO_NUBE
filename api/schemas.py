from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class PacienteCreate(BaseModel):
    nombre: Any = None
    apellido: Any = None
    ci: Any = None
    codigo_paciente: Any = None
    model_config = ConfigDict(extra='allow')

class FiliacionCreate(BaseModel):
    paciente_id: Any = None
    edad: Any = None
    sexo: Any = None
    fecha_nacimiento: Any = None
    lugar_nacimiento: Any = None
    domicilio: Any = None
    n_casa: Any = None
    zona_barrio: Any = None
    ciudad: Any = None
    pais: Any = None
    telefono: Any = None
    estado_civil: Any = None
    profesion_oficio: Any = None
    model_config = ConfigDict(extra='allow')
