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
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
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
    __tablename__ = "declaraciones_p2"
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
    __tablename__ = "declaraciones_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    # Campos de la captura 
    fuma = Column(String)
    alcohol = Column(String)
    drogas = Column(String)
    coca = Column(String)
    deporte = Column(String)
    grupo_sanguineo = Column(String)
    historia_laboral = Column(Text) # JSON con los empleos
    riesgos_expuestos = Column(Text) # JSON con los riesgos marcados
    observaciones = Column(Text)
