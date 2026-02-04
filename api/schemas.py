from pydantic import BaseModel
from typing import Optional

# --- ESQUEMAS DE PACIENTE ---
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

# --- ESQUEMAS DE PARTE 1: FILIACIÓN ---
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

# --- ESQUEMAS DE PARTE 2: ANTECEDENTES (22 CAMPOS REALES) ---
class AntecedentesP2Base(BaseModel):
    paciente_id: int
    p1: str; d1: str
    p2: str; d2: str
    p3: str; d3: str
    p4: str; d4: str
    p5: str; d5: str
    p6: str; d6: str
    p7: str; d7: str
    p8: str; d8: str
    p9: str; d9: str
    p10: str; d10: str
    p11: str; d11: str
    p12: str; d12: str
    p13: str; d13: str
    p14: str; d14: str
    p15: str; d15: str
    p16: str; d16: str
    p17: str; d17: str
    p18: str; d18: str
    p19: str; d19: str
    p20: str; d20: str
    p21: str; d21: str
    p22: str; d22: str

class AntecedentesP2Create(AntecedentesP2Base):
    pass

class AntecedentesP2(AntecedentesP2Base):
    id: int
    class Config:
        from_attributes = True
