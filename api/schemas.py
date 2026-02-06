from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: int
    sexo: str
    fecha_nacimiento: date
    estado_civil: str
    lugar_nacimiento: Optional[str] = "S/D"
    domicilio: Optional[str] = "S/D"
    n_casa: Optional[str] = "S/N"
    zona_barrio: Optional[str] = "S/D"
    ciudad: Optional[str] = "S/D"
    pais: Optional[str] = "BOLIVIA"
    telefono: Optional[str] = "0"
    profesion_oficio: Optional[str] = "S/D"

class AntecedentesCreate(BaseModel):
    paciente_id: int
    p1: str; d1: str; p2: str; d2: str; p3: str; d3: str; p4: str; d4: str; p5: str; d5: str
    p6: str; d6: str; p7: str; d7: str; p8: str; d8: str; p9: str; d9: str; p10: str; d10: str
    p11: str; d11: str; p12: str; d12: str; p13: str; d13: str; p14: str; d14: str; p15: str; d15: str
    p16: str; d16: str; p17: str; d17: str; p18: str; d18: str

class HabitosCreate(BaseModel):
    paciente_id: int
    deportes_si_no: str
    deportes_detalle: str
    accidentes_si_no: str
    accidentes_detalle: str
    medicamentos_si_no: str
    medicamentos_detalle: str
    grupo_sanguineo: str
    historia_laboral: str
