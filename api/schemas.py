from pydantic import BaseModel
from typing import Optional
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
    p1: str = "INFO"; d1: Optional[str] = "NORMAL"
    p2: str = "INFO"; d2: Optional[str] = "NORMAL"
    p3: str = "INFO"; d3: Optional[str] = "NORMAL"
    p4: str = "INFO"; d4: Optional[str] = "NORMAL"
    p5: str = "INFO"; d5: Optional[str] = "NORMAL"
    p6: str = "INFO"; d6: Optional[str] = "NORMAL"
    p7: str = "INFO"; d7: Optional[str] = "NORMAL"
    p8: str = "INFO"; d8: Optional[str] = "NORMAL"
    p9: str = "INFO"; d9: Optional[str] = "NORMAL"
    p10: str = "INFO"; d10: Optional[str] = "NORMAL"
    p11: str = "INFO"; d11: Optional[str] = "NORMAL"
    p12: str = "INFO"; d12: Optional[str] = "NORMAL"
    p13: str = "INFO"; d13: Optional[str] = "NORMAL"
    p14: str = "INFO"; d14: Optional[str] = "NINGUNA"
    p15: str = "INFO"; d15: Optional[str] = "NINGUNA"
    p16: str = "INFO"; d16: Optional[str] = "NINGUNA"
    p17: str = "INFO"; d17: Optional[str] = "NINGUNA"
    p18: str = "INFO"; d18: Optional[str] = "NINGUNA"
    p19: str = "INFO"; d19: Optional[str] = "NINGUNA"
    p20: str = "INFO"; d20: Optional[str] = "NINGUNA"
    p21: str = "INFO"; d21: Optional[str] = "NINGUNA"
    p22: str = "INFO"; d22: Optional[str] = "NINGUNA"

class HabitosCreate(BaseModel):
    paciente_id: int
    fuma: str = "NO"
    bebe: str = "NO"
    drogas: str = "NO"
    coca: str = "NO"
    deportes: Optional[str] = "NINGUNO"
    grupo_sanguineo: Optional[str] = "S/D"
