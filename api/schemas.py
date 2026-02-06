from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    ci: str
    codigo_paciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    class Config:
        from_attributes = True

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: int
    sexo: str
    fecha_nacimiento: date
    domicilio: Optional[str] = "S/D"
    n_casa: Optional[str] = "S/N"
    ciudad: Optional[str] = "S/D"
    pais: Optional[str] = "BOLIVIA"
    telefono: Optional[str] = "0"
    estado_civil: str
    profesion_oficio: Optional[str] = "S/D"

class AntecedentesCreate(BaseModel):
    paciente_id: int
    p1: str; d1: str; p2: str; d2: str; p3: str; d3: str; p4: str; d4: str; p5: str; d5: str
    p6: str; d6: str; p7: str; d7: str; p8: str; d8: str; p9: str; d9: str; p10: str; d10: str
    p11: str; d11: str; p12: str; d12: str; p13: str; d13: str; p14: str; d14: str; p15: str; d15: str
    p16: str; d16: str; p17: str; d17: str; p18: str; d18: str

class HabitosCreate(BaseModel):
    paciente_id: int
    h1: Optional[str] = "NO"; r1: Optional[str] = ""
    h2: Optional[str] = "NO"; r2: Optional[str] = ""
    h3: Optional[str] = "NO"; r3: Optional[str] = ""
    h4: Optional[str] = "NO"; r4: Optional[str] = ""
    h5: Optional[str] = "NO"; r5: Optional[str] = ""
    h6: Optional[str] = "NO"; r6: Optional[str] = ""
    h7: Optional[str] = "NO"; r7: Optional[str] = ""
    h8: Optional[str] = "NO"; r8: Optional[str] = ""
    h9: Optional[str] = "NO"; r9: Optional[str] = ""
    h10: Optional[str] = "NO"; r10: Optional[str] = ""
    historia_laboral: Optional[str] = "[]"
