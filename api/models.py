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
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
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
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
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
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
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
    historia_laboral = Column(Text)  # Guarda el JSON de la tabla
    riesgos_expuestos = Column(Text) # Guarda el JSON de los checks
    observaciones = Column(String)
