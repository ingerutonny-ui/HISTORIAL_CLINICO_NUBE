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
    lugar_nacimiento: Optional[str] = "S/D"
    domicilio: Optional[str] = "S/D"
    n_casa: Optional[str] = "S/N"
    zona_barrio: Optional[str] = "S/D"
    ciudad: Optional[str] = "S/D"
    pais: Optional[str] = "BOLIVIA"
    telefono: Optional[str] = "00000000"
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
    h1: str; r1: str; h2: str; r2: str; h3: str; r3: str; h4: str; r4: str; h5: str; r5: str
    h6: str; r6: str; h7: str; r7: str; h8: str; r8: str; h9: str; r9: str; h10: str; r10: str
    historia_laboral: Optional[str] = "[]"
