from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    documento_identidad: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    codigo_paciente: str
    class Config:
        from_attributes = True
