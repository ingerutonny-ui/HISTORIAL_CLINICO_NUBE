from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# --- ESQUEMAS PARA PACIENTE (REGISTRO INICIAL) ---
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
# Coincide con la sección 'AFILIACION DEL TRABAJADOR' del PDF [cite: 5]
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
# Coincide con las secciones de enfermedades (VISTA, AUDITIVO, etc.) [cite: 24, 25, 26]
class AntecedentesCreate(BaseModel):
    paciente_id: int
    # P=Pregunta (SI/NO), D=Detalle/Observación
    p1: str = "NO"  # Vista [cite: 25]
    d1: Optional[str] = ""
    p2: str = "NO"  # Auditivo [cite: 26]
    d2: Optional[str] = ""
    p3: str = "NO"  # Respiratorios [cite: 27]
    d3: Optional[str] = ""
    p4: str = "NO"  # Cardio-vasculares [cite: 28]
    d4: Optional[str] = ""
    p5: str = "NO"  # Estómago/Intestino [cite: 29]
    d5: Optional[str] = ""
    p6: str = "NO"  # Sangre [cite: 29, 43]
    d6: Optional[str] = ""
    p7: str = "NO"  # Genito-urinario [cite: 30]
    d7: Optional[str] = ""
    p8: str = "NO"  # ITS [cite: 45]
    d8: Optional[str] = ""
    p9: str = "NO"  # Sistema Nervioso [cite: 31]
    d9: Optional[str] = ""
    p10: str = "NO" # Psiquiátricos [cite: 32]
    d10: Optional[str] = ""
    p11: str = "NO" # Osteomusculares [cite: 47]
    d11: Optional[str] = ""
    p12: str = "NO" # Endocrinológicos [cite: 48]
    d12: Optional[str] = ""
    cirugias: Optional[str] = "NINGUNA" [cite: 63]
    accidentes: Optional[str] = "NINGUNO" [cite: 67]

# --- ESQUEMA PARA PARTE 3: HÁBITOS ---
# Coincide con la sección 'HABITOS' del PDF (Alcohol, Tabaco, Drogas) [cite: 77, 82, 83, 84]
class HabitosCreate(BaseModel):
    paciente_id: int
    fuma: str = "NO" [cite: 83]
    bebe: str = "NO" [cite: 82]
    drogas: str = "NO" [cite: 84]
    coca: str = "NO" [cite: 86]
    deportes: Optional[str] = "NINGUNO" [cite: 76]
    grupo_sanguineo: Optional[str] = "S/D" [cite: 73]
