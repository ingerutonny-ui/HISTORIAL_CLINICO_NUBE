from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
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
    
    # --- ANTECEDENTES PATOLÓGICOS (Campos de texto para detallar) ---
    vista = Column(Text, nullable=True)
    auditivo = Column(Text, nullable=True)
    respiratorios = Column(Text, nullable=True)
    cardiovasculares = Column(Text, nullable=True)
    digestivos = Column(Text, nullable=True)
    genitourinario = Column(Text, nullable=True)
    sistema_nervioso = Column(Text, nullable=True)
    osteomusculares = Column(Text, nullable=True)
    endocrinos = Column(Text, nullable=True)
    dermatologicos = Column(Text, nullable=True)
    
    # --- ALERGIAS E INFECCIONES ---
    alergias_medicamentos = Column(Text, nullable=True)
    chagas = Column(String, nullable=True) # SI / NO
    hepatitis = Column(String, nullable=True) # SI / NO
    
    # --- ANTECEDENTES PERSONALES ---
    cirugias = Column(Text, nullable=True)
    accidentes_trabajo = Column(Text, nullable=True)
    accidentes_particulares = Column(Text, nullable=True)
    medicamentos_uso_actual = Column(Text, nullable=True)
    grupo_sanguineo = Column(String, nullable=True)
    deportes = Column(Text, nullable=True)
    
    # --- HÁBITOS (Consumo y Frecuencia) ---
    alcohol = Column(String, nullable=True)
    tabaco = Column(String, nullable=True)
    drogas = Column(String, nullable=True)
    coca_bolo = Column(String, nullable=True)
    
    # --- HISTORIA LABORAL ---
    edad_inicio_trabajo = Column(Integer, nullable=True)
    empresa_actual = Column(String, nullable=True)
    ocupacion_actual = Column(String, nullable=True)
    tiempo_trabajo = Column(String, nullable=True)
    riesgos_expuestos = Column(Text, nullable=True) # Ruido, Polvo, etc.
    uso_epp = Column(String, nullable=True) # SI / NO

    paciente = relationship("Paciente", back_populates="declaraciones")
