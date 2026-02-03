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
    
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")

class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))

    # --- SECCIÓN 1: AFILIACIÓN DEL TRABAJADOR ---
    edad = Column(Integer, nullable=True)
    sexo = Column(String, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)
    fecha_nacimiento = Column(String, nullable=True)
    estado_civil = Column(String, nullable=True)
    domicilio = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    profesion_oficio = Column(String, nullable=True)

    # --- SECCIÓN 2: ANTECEDENTES PATOLÓGICOS (Texto para detalles) ---
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
    alergias_medicamentos = Column(Text, nullable=True)
    chagas = Column(Text, nullable=True)
    otros_antecedentes = Column(Text, nullable=True)

    # --- SECCIÓN 3: HISTORIA LABORAL Y HÁBITOS ---
    # Hábitos
    fuma = Column(Boolean, default=False)
    fuma_detalle = Column(String, nullable=True)
    bebe = Column(Boolean, default=False)
    bebe_detalle = Column(String, nullable=True)
    drogas = Column(Boolean, default=False)
    drogas_detalle = Column(String, nullable=True)
    bolo_coca = Column(Boolean, default=False)
    bolo_coca_detalle = Column(String, nullable=True)
    
    # Historia Laboral
    edad_inicio_laboral = Column(Integer, nullable=True)
    empresa_actual = Column(String, nullable=True)
    riesgos_expuestos = Column(Text, nullable=True) # Ruido, Polvo, Gases, etc.
    uso_epp = Column(Boolean, default=False)
    epp_detalle = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="declaraciones")
