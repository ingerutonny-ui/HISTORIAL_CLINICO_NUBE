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
    zona = Column(String) # Unificado de zona_barrio a zona
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    estado_civil = Column(String)
    profesion = Column(String) # Unificado de profesion_oficio a profesion

class AntecedentesP2(Base):
    __tablename__ = "declaraciones_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    vista = Column(String)
    vista_obs = Column(Text, default="")
    auditivo = Column(String)
    auditivo_obs = Column(Text, default="")
    respiratorio = Column(String)
    respiratorio_obs = Column(Text, default="")
    cardiovasculares = Column(String) # Unificado de cardio
    cardiovasculares_obs = Column(Text, default="")
    digestivos = Column(String)
    digestivos_obs = Column(Text, default="")
    sangre = Column(String)
    sangre_obs = Column(Text, default="")
    genitourinario = Column(String)
    genitourinario_obs = Column(Text, default="")
    sistema_nervioso = Column(String)
    sistema_nervioso_obs = Column(Text, default="")
    psiquiatricos = Column(String)
    psiquiatricos_obs = Column(Text, default="")
    osteomusculares = Column(String)
    osteomusculares_obs = Column(Text, default="")
    endocrino = Column(String)
    endocrino_obs = Column(Text, default="")
    alergias = Column(String)
    alergias_obs = Column(Text, default="")
    cirugias = Column(String)
    cirugias_obs = Column(Text, default="")
    accidentes_trabajo = Column(String) # Unificado de acc_trabajo
    accidentes_trabajo_obs = Column(Text, default="")
    accidentes_pers = Column(String) # Unificado de acc_personales
    accidentes_pers_obs = Column(Text, default="")
    medicamentos = Column(String)
    medicamentos_obs = Column(Text, default="")
    infecciosas = Column(String) # Unificado de infecciones
    infecciosas_obs = Column(Text, default="")
    ap_urinario = Column(String, default="NO")
    ap_urinario_obs = Column(Text, default="")
    linfatico = Column(String, default="NO")
    linfatico_obs = Column(Text, default="")
    reumatologicos = Column(String)
    reumatologicos_obs = Column(Text, default="")
    otros = Column(String, default="NO")
    otros_obs = Column(Text, default="")
    generales = Column(String)
    generales_obs = Column(Text, default="")

class HabitosRiesgosP3(Base):
    __tablename__ = "declaraciones_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fuma = Column(String)
    bebe_alcohol = Column(String)
    deporte = Column(String)
    observaciones = Column(Text)
