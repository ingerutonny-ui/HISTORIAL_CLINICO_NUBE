from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from datetime import date

# Lo que el Frontend envía (Formulario Inicial)
class PacienteCreate(BaseModel):
    nombres: str
    apellidos: str
    documento_identidad: str

# Lo que el Backend responde (Incluye el código generado)
class PacienteResponse(BaseModel):
    id: int
    codigo_paciente: str
    fecha_ingreso: datetime
    nombres: str
    apellidos: str
    documento_identidad: str

    class Config:
        from_attributes = True
