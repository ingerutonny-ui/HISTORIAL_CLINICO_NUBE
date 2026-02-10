from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)  # Sincronizado con el frontend
    apellido = Column(String, index=True)
    ci = Column(String, unique=True, index=True)
    codigo_paciente = Column(String, unique=True, index=True)

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    
    # P1 - Datos Médicos
    operaciones = Column(Text)
    enfermedades = Column(Text)
    medicamentos = Column(Text)
    alergias = Column(Text)

class AntecedentesP2(Base):
    __tablename__ = "antecedentes_p2"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    
    # P2 - Antecedentes
    ant_patologicos = Column(Text)
    ant_no_patologicos = Column(Text)
    ant_familiares = Column(Text)

class HabitosRiesgosP3(Base):
    __tablename__ = "habitos_riesgos_p3"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    
    # P3 - Hábitos e Historia Laboral
    fuma = Column(String)
    alcohol = Column(String)
    drogas = Column(String)
    pijchar = Column(String)
    deportes = Column(String)
    grupo_sanguineo = Column(String)
    historia_laboral = Column(Text)  # JSON de empleos
    
    # Riesgos (Sincronizado con tu captura de checkboxes)
    ruido = Column(Boolean, default=False)
    polvos = Column(Boolean, default=False)
    vibracion = Column(Boolean, default=False)
    gases_vapores = Column(Boolean, default=False)
    radiacion = Column(Boolean, default=False)
    ergonomicos = Column(Boolean, default=False)
    temp_extremas = Column(Boolean, default=False)
    psicosocial = Column(Boolean, default=False)
