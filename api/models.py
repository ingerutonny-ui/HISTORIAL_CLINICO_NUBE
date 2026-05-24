from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    ci = Column(String, unique=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_p1"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    edad = Column(String)
    sexo = Column(String)
    fecha_nacimiento = Column(String)
    lugar_nacimiento = Column(String)
    domicilio = Column(String)
    n_casa = Column(String)
    zona_barrio = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    estado_civil = Column(String)
    profesion_oficio = Column(String)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    vista = Column(String)
    auditivo = Column(String)
    respiratorio = Column(String)
    cardio = Column(String)
    digestivos = Column(String)
    sangre = Column(String)
    genitourinario = Column(String)
    sistema_nervioso = Column(String)
    psiquiatricos = Column(String)
    osteomusculares = Column(String)
    reumatologicos = Column(String)
    dermatologicas = Column(String)
    alergias = Column(String)
    cirugias = Column(String)
    infecciones = Column(String)
    acc_personales = Column(String)
    acc_trabajo = Column(String)
    medicamentos = Column(String)
    endocrino = Column(String)
    familiares = Column(String)
    otros_especificos = Column(String)
    generales = Column(String)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    fuma = Column(String)
    fuma_cantidad = Column(String)
    alcohol = Column(String)
    alcohol_frecuencia = Column(String)
    drogas = Column(String)
    drogas_tipo = Column(String)
    coca = Column(String)
    deporte = Column(String)
    deporte_detalle = Column(String)
    grupo_sanguineo = Column(String)
    historia_laboral = Column(Text)
    riesgos_expuestos = Column(Text)
    observaciones = Column(String)

class Enfermera(Base):
    __tablename__ = "enfermeras"
    id_enfe = Column(Integer, primary_key=True, index=True)
    ci_enfe = Column(String, unique=True)
    appaterno_enfe = Column(String)
    apmaterno_enfe = Column(String)
    nombre_enfe = Column(String)
    turno_enfe = Column(String)
    edu_enfe = Column(String)
    especialidad = Column(String)

class Doctor(Base):
    __tablename__ = "doctores"
    id_doc = Column(Integer, primary_key=True, index=True)
    ci_doc = Column(String, unique=True)
    appaterno_doc = Column(String)
    apmaterno_doc = Column(String)
    nombre_doc = Column(String)
    turno_doc = Column(String)
    especialidad = Column(String)

class FichaOftalmologica(Base):
    __tablename__ = "ficha_oftalmologica"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    
    # Antecedentes
    lentes = Column(String)
    daltonismo = Column(String)
    diabetes = Column(String)
    estrabismo = Column(String)
    infecciones = Column(String)
    presion_alta = Column(String)
    obs_ant = Column(Text)
    
    # Examen Clínico
    anamnesis = Column(String)
    ana_obs = Column(Text)
    examen_externo = Column(String)
    exe_obs = Column(Text)
    
    # Agudeza Visual
    od_l_sc = Column(String); od_l_cc = Column(String); od_l_dio = Column(String)
    oi_l_sc = Column(String); oi_l_cc = Column(String); oi_l_dio = Column(String)
    od_c_sc = Column(String); od_c_cc = Column(String); od_c_dio = Column(String)
    oi_c_sc = Column(String); oi_c_cc = Column(String); oi_c_dio = Column(String)
    
    # Exámenes Complementarios
    cv_od = Column(String); cv_od_obs = Column(Text)
    cv_oi = Column(String); cv_oi_obs = Column(Text)
    fo = Column(String); fo_obs = Column(Text)
    ish = Column(String); ish_obs = Column(Text)
    est = Column(String); est_obs = Column(Text)
    
    # Presión y Diagnóstico
    pio_od = Column(String); pio_oi = Column(String); pio_obs = Column(String)
    diagnostico = Column(Text)
