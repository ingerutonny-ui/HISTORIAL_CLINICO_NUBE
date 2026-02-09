from pydantic import BaseModel

class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    ci: str
    codigo_paciente: str

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
    reumatologicos: str
    dermatologicas: str
    alergias: str
    cirugias: str
    infecciones: str
    acc_personales: str
    acc_trabajo: str
    medicamentos: str
    endocrino: str
    familiares: str
    otros_especificos: str
    generales: str
