from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class PacienteCreate(BaseModel):
    nombres: str
    apellidos: str
    ci: str
    codigo_paciente: str

class Paciente(PacienteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: int
    sexo: str
    fecha_nacimiento: date
    estado_civil: str
    lugar_nacimiento: str
    domicilio: str
    n_casa: str
    zona_barrio: str
    ciudad: str
    pais: str
    telefono: str
    profesion_oficio: str

class AntecedentesCreate(BaseModel):
    paciente_id: int
    p1: str; d1: str; p2: str; d2: str; p3: str; d3: str; p4: str; d4: str; p5: str; d5: str
    p6: str; d6: str; p7: str; d7: str; p8: str; d8: str; p9: str; d9: str; p10: str; d10: str
    p11: str; d11: str; p12: str; d12: str; p13: str; d13: str; p14: str; d14: str; p15: str; d15: str
    p16: str; d16: str; p17: str; d17: str; p18: str; d18: str

class HabitosCreate(BaseModel):
    paciente_id: int
    fuma_si_no: str
    fuma_detalle: str
    alcohol_si_no: str
    alcohol_detalle: str
    drogas_si_no: str
    drogas_detalle: str
    pijchar_si_no: str
    deportes_si_no: str
    deportes_detalle: str
    grupo_sanguineo: str
    accidentes_si_no: str
    accidentes_detalle: str
    medicamentos_si_no: str
    medicamentos_detalle: str
    riesgos_vida_laboral: str
    historia_laboral: str
