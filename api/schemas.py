from pydantic import BaseModel
from typing import Optional, List

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

class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    edad: str
    sexo: str
    fecha_nacimiento: str
    lugar_nacimiento: str
    domicilio: str
    n_casa: str
    zona_barrio: str
    ciudad: str
    pais: str
    telefono: str
    estado_civil: str
    profesion_oficio: str

class DeclaracionJuradaCreate(DeclaracionJuradaBase):
    pass

class DeclaracionJurada(DeclaracionJuradaBase):
    id: int
    class Config:
        from_attributes = True
