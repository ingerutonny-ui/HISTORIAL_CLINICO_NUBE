from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    ci = Column(String, unique=True)
    codigo_paciente = Column(String)

class DeclaracionJurada(Base):
    __tablename__ = "filiacion"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    edad = Column(Integer); sexo = Column(String); fecha_nacimiento = Column(Date)
    estado_civil = Column(String); lugar_nacimiento = Column(String)
    domicilio = Column(String); n_casa = Column(String); zona_barrio = Column(String)
    ciudad = Column(String); pais = Column(String); telefono = Column(String)
    profesion_oficio = Column(String)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    vista = Column(String); auditivo = Column(String); respiratorio = Column(String)
    cardio = Column(String); estomago = Column(String); sangre = Column(String)
    genito = Column(String); nervioso = Column(String); psiquiatrico = Column(String)
    osteo = Column(String); endocrino = Column(String); reumato = Column(String)
    generales = Column(String); dermato = Column(String); alergias = Column(String)
    infecciosas = Column(String); cirugias = Column(String); acc_trabajo = Column(String)
    acc_personales = Column(String); medicamentos = Column(String); familiares = Column(String)
    otros = Column(String)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_riesgos_p3"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fuma_si_no = Column(String); fuma_detalle = Column(String)
    alcohol_si_no = Column(String); alcohol_detalle = Column(String)
    drogas_si_no = Column(String); drogas_detalle = Column(String)
    pijchar_si_no = Column(String); deportes_si_no = Column(String)
    deportes_detalle = Column(String); grupo_sanguineo = Column(String)
    accidentes_si_no = Column(String); accidentes_detalle = Column(String)
    medicamentos_si_no = Column(String); medicamentos_detalle = Column(String)
    alergias_si_no = Column(String); alergias_detalle = Column(String)
    riesgos_vida_laboral = Column(String); historia_laboral = Column(String)
