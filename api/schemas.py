from pydantic import BaseModel
from typing import Optional

# Esquemas para Pacientes (Necesarios para el Registro)
class PacienteCreate(BaseModel):
    nombres: str
    apellidos: str
    documento_identidad: str
    codigo_paciente: str

class Paciente(PacienteCreate):
    id: int
    class Config:
        from_attributes = True

# Esquemas para Declaración Jurada
class DeclaracionJuradaCreate(BaseModel):
    paciente_id: int
    edad: Optional[int] = None
    sexo: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    estado_civil: Optional[str] = None
    domicilio: Optional[str] = None
    telefono: Optional[str] = None
    profesion_oficio: Optional[str] = None

class DeclaracionJurada(DeclaracionJuradaCreate):
    id: int
    class Config:
        from_attributes = True
