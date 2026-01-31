from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)
    apellidos = Column(String)
    documento_identidad = Column(String, unique=True, index=True)
    codigo_paciente = Column(String, unique=True)
    
    # Relación con las declaraciones juradas
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # --- SECCIÓN 1: AFILIACIÓN ---
    edad = Column(Integer, nullable=True)
    sexo = Column(String, nullable=True)
    fecha_nacimiento = Column(String, nullable=True) # Se guarda como string para evitar conflictos de formato
    lugar_nacimiento = Column(String, nullable=True)
    domicilio_av_calle = Column(String, nullable=True)
    domicilio_numero = Column(String, nullable=True)
    barrio = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    estado_civil = Column(String, nullable=True)
    profesion_labor = Column(String, nullable=True)

    # --- SECCIÓN 2: ANTECEDENTES DE SALUD ---
    vista = Column(String, default="NO")
    auditivo = Column(String, default="NO")
    respiratorios = Column(String, default="NO")
    cardio = Column(String, default="NO")
    digestivo = Column(String, default="NO")
    sangre = Column(String, default="NO")
    urinario = Column(String, default="NO")
    nervioso = Column(String, default="NO")
    psiquiatrico = Column(String, default="NO")
    oseo = Column(String, default="NO")
    metabolico = Column(String, default="NO")
    reuma = Column(String, default="NO")
    generales = Column(String, default="NO")
    piel = Column(String, default="NO")
    infecciones = Column(String, default="NO")
    
    alergia_med = Column(Text, nullable=True)
    alergia_ali = Column(Text, nullable=True)

    # --- SECCIÓN 3.1: HÁBITOS ---
    h_alc_sn = Column(String, nullable=True)
    h_alc_cant = Column(String, nullable=True)
    h_alc_freq = Column(String, nullable=True)
    
    h_tab_sn = Column(String, nullable=True)
    h_tab_cant = Column(String, nullable=True)
    h_tab_freq = Column(String, nullable=True)
    
    h_coca_sn = Column(String, nullable=True)
    h_coca_cant = Column(String, nullable=True)
    h_coca_freq = Column(String, nullable=True)

    # --- SECCIÓN 3.2: HISTORIA LABORAL ---
    historia_laboral = Column(Text, nullable=True)

    # --- SECCIÓN 3.3: LOS 17 RIESGOS DETALLADOS ---
    r_ruido = Column(String, nullable=True)
    r_radiacion = Column(String, nullable=True)
    r_vibracion = Column(String, nullable=True)
    r_mecanicos = Column(String, nullable=True)
    r_temperatura = Column(String, nullable=True)
    r_polvo = Column(String, nullable=True)
    r_humos = Column(String, nullable=True)
    r_gases = Column(String, nullable=True)
    r_metales = Column(String, nullable=True)
    r_plomo = Column(String, nullable=True)
    r_repetitivos = Column(String, nullable=True)
    r_carga = Column(String, nullable=True)
    r_psicologico = Column(String, nullable=True)
    r_biologico = Column(String, nullable=True)
    r_altura = Column(String, nullable=True)
    r_confinados = Column(String, nullable=True)
    r_otros = Column(String, nullable=True)
    
    observaciones = Column(Text, nullable=True)

    paciente = relationship("Paciente", back_populates="declaraciones")
