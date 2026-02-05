from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- ESQUEMAS PARA PACIENTE ---
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

# --- ESQUEMA PARA PARTE 1: FILIACIÓN ---
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

# --- ESQUEMA PARA PARTE 2: ANTECEDENTES ---
class AntecedentesCreate(BaseModel):
    paciente_id: int
    p1: str = "NO"
    d1: Optional[str] = ""
    p2: str = "NO"
    d2: Optional[str] = ""
    p3: str = "NO"
    d3: Optional[str] = ""
    p4: str = "NO"
    d4: Optional[str] = ""
    p5: str = "NO"
    d5: Optional[str] = ""
    p6: str = "NO"
    d6: Optional[str] = ""
    p7: str = "NO"
    d7: Optional[str] = ""
    p8: str = "NO"
    d8: Optional[str] = ""
    p9: str = "NO"
    d9: Optional[str] = ""
    p10: str = "NO"
    d10: Optional[str] = ""
    p11: str = "NO"
    d11: Optional[str] = ""
    p12: str = "NO"
    d12: Optional[str] = ""
    cirugias: Optional[str] = "NINGUNA"
    accidentes: Optional[str] = "NINGUNO"

# --- ESQUEMA PARA PARTE 3: HÁBITOS ---
class HabitosCreate(BaseModel):
    paciente_id: int
    fuma: str = "NO"
    bebe: str = "NO"
    drogas: str = "NO"
    coca: str = "NO"
    deportes: Optional[str] = "NINGUNO"
    grupo_sanguineo: Optional[str] = "S/D"
