from pydantic import BaseModel
from typing import Optional

class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str

class Paciente(PacienteCreate):
    id: int
    class Config:
        orm_mode = True

class FiliacionCreate(BaseModel):
    paciente_id: int
    edad: int
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

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: str
    auditivo: str
    respiratorio: str
    cardio: str
    digestivos: str
    sangre: str
    genitourinario: str
    sistema_nervioso: str
    psiquiatricos: str
    osteomusculares: str
    endocrino: str
    alergias: str
    cirugias: str
    acc_trabajo: str
    acc_personales: str
    medicamentos: str
    infecciosas: str
    ap_urinario: str
    linfatico: str
    reumatologicos: str
    otros: str
    generales: str
