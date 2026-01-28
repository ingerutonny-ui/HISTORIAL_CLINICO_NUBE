from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Esquema base para compartir campos comunes
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    historia_clinica: Optional[str] = None

# Esquema para la creación (lo que recibimos del Frontend)
class PacienteCreate(PacienteBase):
    # El codigo_paciente se generará en la lógica antes de guardar
    pass

# Esquema para la respuesta (lo que el API devuelve)
class Paciente(PacienteBase):
    id: int
    codigo_paciente: str
    fecha_registro: datetime

    class Config:
        from_attributes = True
