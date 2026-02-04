from pydantic import BaseModel
from typing import Optional, List

# Esquemas para Paciente
class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    documento_identidad: str
    codigo_paciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# Esquemas para Declaración Jurada (Parte 1)
class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    edad: Optional[int] = None
    sexo: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    estado_civil: Optional[str] = None
    domicilio: Optional[str] = None
    telefono: Optional[str] = None
    profesion_oficio: Optional[str] = None

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    class Config:
        from_attributes = True
