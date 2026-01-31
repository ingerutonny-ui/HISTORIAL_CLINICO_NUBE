from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
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

    # --- SECCIÓN 1: DATOS COMPLEMENTARIOS ---
    domicilio_av_calle = Column(String, nullable=True)
    domicilio_numero = Column(String, nullable=True)
    barrio = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    profesion_labor = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    estado_civil = Column(String, nullable=True)

    # --- SECCIÓN 2: ANTECEDENTES PATOLÓGICOS ---
    vista = Column(Text, nullable=True)
    auditivo = Column(Text, nullable=True)
    respiratorios = Column(Text, nullable=True)
    cardiovasculares = Column(Text, nullable=True)
    estomago_intestino = Column(Text, nullable=True)
    sangre = Column(Text, nullable=True)
    genitourinario = Column(Text, nullable=True)
    sistema_nervioso = Column(Text, nullable=True)
    psiquiatricos_mentales = Column(Text, nullable=True)
    osteomusculares = Column(Text, nullable=True)
    endocrinos_metabolicos = Column(Text, nullable=True)
    reumatologicos = Column(Text, nullable=True)
    dermatologicos = Column(Text, nullable=True)
    generales_cancer_hernias = Column(Text, nullable=True)

    # ALERGIAS E INFECCIONES
    alergias_medicamentos = Column(Text, nullable=True)
    alergias_alimentos = Column(Text, nullable=True)
    infecciones_detalle = Column(Text, nullable=True)
    
    # --- SECCIÓN 3: PERSONALES, HÁBITOS Y LABORAL ---
    cirugias = Column(Text, nullable=True)
    accidentes_trabajo = Column(Text, nullable=True)
    accidentes_particulares = Column(Text, nullable=True)
    medicamentos_uso_actual = Column(Text, nullable=True)
    grupo_sanguineo = Column(String, nullable=True)
    deportes = Column(Text, nullable=True)
    
    alcohol = Column(String, nullable=True)
    tabaco = Column(String, nullable=True)
    drogas = Column(String, nullable=True)
    coca_bolo = Column(String, nullable=True)
    
    edad_inicio_trabajo = Column(Integer, nullable=True)
    historia_laboral_detalle = Column(Text, nullable=True)
    riesgos_expuestos = Column(Text, nullable=True)
    uso_epp = Column(String, nullable=True)

    # --- CIERRE ---
    observaciones = Column(Text, nullable=True)
    
    paciente = relationship("Paciente", back_populates="declaraciones")
