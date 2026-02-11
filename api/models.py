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
    vista = Column(String, default="NORMAL")
    auditivo = Column(String, default="NORMAL")
    respiratorio = Column(String, default="NORMAL")
    cardio = Column(String, default="NORMAL")
    digestivos = Column(String, default="NORMAL")
    sangre = Column(String, default="NORMAL")
    genitourinario = Column(String, default="NORMAL")
    sistema_nervioso = Column(String, default="NORMAL")
    psiquiatricos = Column(String, default="NORMAL")
    osteomusculares = Column(String, default="NORMAL")
    reumatologicos = Column(String, default="NORMAL")
    dermatologicas = Column(String, default="NORMAL")
    alergias = Column(String, default="NORMAL")
    cirugias = Column(String, default="NORMAL")
    infecciones = Column(String, default="NORMAL")
    acc_personales = Column(String, default="NORMAL")
    acc_trabajo = Column(String, default="NORMAL")
    medicamentos = Column(String, default="NORMAL")
    endocrino = Column(String, default="NORMAL")
    familiares = Column(String, default="NORMAL")
    otros_especificos = Column(String, default="NORMAL")
    generales = Column(String, default="NORMAL")

class HabitosRiesgosP3(Base):
    __tablename__ = "declaraciones_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fuma = Column(String, default="NO")
    fuma_cantidad = Column(String, default="")
    alcohol = Column(String, default="NO")
    alcohol_frecuencia = Column(String, default="")
    drogas = Column(String, default="NO")
    drogas_tipo = Column(String, default="")
    coca = Column(String, default="NO")
    deporte = Column(String, default="NO")
    deporte_detalle = Column(String, default="")
    grupo_sanguineo = Column(String, default="")
    historia_laboral = Column(Text, default="[]") 
    riesgos_expuestos = Column(Text, default="[]")
    observaciones = Column(Text, default="SIN OBSERVACIONES")
