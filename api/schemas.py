from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class PacienteCreate(BaseModel):
    nombres: str; apellidos: str; ci: str; codigo_paciente: str

class Paciente(PacienteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FiliacionCreate(BaseModel):
    paciente_id: int; edad: int; sexo: str; fecha_nacimiento: date; estado_civil: str
    lugar_nacimiento: str; domicilio: str; n_casa: str; zona_barrio: str; ciudad: str
    pais: str; telefono: str; profesion_oficio: str

class AntecedentesCreate(BaseModel):
    paciente_id: int
    vista: str; auditivo: str; respiratorio: str; cardio: str; estomago: str
    sangre: str; genito: str; nervioso: str; psiquiatrico: str; osteo: str
    endocrino: str; reumato: str; generales: str; dermato: str; alergias: str
    infecciosas: str; cirugias: str; acc_trabajo: str; acc_personales: str
    medicamentos: str; familiares: str; otros: str

class HabitosCreate(BaseModel):
    paciente_id: int; fuma_si_no: str; fuma_detalle: str; alcohol_si_no: str
    alcohol_detalle: str; drogas_si_no: str; drogas_detalle: str; pijchar_si_no: str
    deportes_si_no: str; deportes_detalle: str; grupo_sanguineo: str
    accidentes_si_no: str; accidentes_detalle: str; medicamentos_si_no: str
    medicamentos_detalle: str; alergias_si_no: str; alergias_detalle: str
    riesgos_vida_laboral: str; historia_laboral: str
