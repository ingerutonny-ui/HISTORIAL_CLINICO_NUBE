from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str
    model_config = ConfigDict(from_attributes=True)

class DeclaracionJuradaBase(BaseModel):
    paciente_id: int
    edad: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    domicilio: Optional[str] = None
    n_casa: Optional[str] = None
    zona_barrio: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    telefono: Optional[str] = None
    estado_civil: Optional[str] = None
    profesion_oficio: Optional[str] = None
    model_config = ConfigDict(from_attributes=True, extra='allow')

class AntecedentesP2Base(BaseModel):
    paciente_id: int
    model_config = ConfigDict(from_attributes=True, extra='allow')

class HabitosRiesgosP3Base(BaseModel):
    paciente_id: int
    model_config = ConfigDict(from_attributes=True, extra='allow')

# --- ESQUEMAS PARA TABLA 5: ENFERMERA ---
class EnfermeraBase(BaseModel):
    ci_enfe: str = Field(..., max_length=10)
    appaterno_enfe: str = Field(..., max_length=15)
    apmaterno_enfe: str = Field(..., max_length=15)
    nombre_enfe: str = Field(..., max_length=15)
    turno_enfe: str  # mañana, tarde, noche
    edu_enfe: str    # tec.med, tec.sup, lic.
    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS PARA TABLA 6: DOCTOR ---
class DoctorBase(BaseModel):
    ci_doc: str = Field(..., max_length=10)
    appaterno_doc: str = Field(..., max_length=15)
    apmaterno_doc: str = Field(..., max_length=15)
    nombre_doc: str = Field(..., max_length=15)
    turno_doc: str   # mañana, tarde, noche
    especialidad: str # Lista de especialidades
    model_config = ConfigDict(from_attributes=True)
