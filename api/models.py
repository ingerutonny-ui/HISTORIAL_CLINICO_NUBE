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

    # --- SECCIÓN 1: DATOS COMPLEMENTARIOS (Pág. 1 PDF) ---
    domicilio_av_calle = Column(String, nullable=True) [cite: 16]
    domicilio_numero = Column(String, nullable=True) [cite: 17]
    barrio = Column(String, nullable=True) [cite: 21]
    ciudad = Column(String, nullable=True) [cite: 18]
    pais = Column(String, nullable=True) [cite: 19]
    profesion_labor = Column(String, nullable=True) [cite: 20]
    telefono = Column(String, nullable=True) [cite: 22]
    estado_civil = Column(String, nullable=True) [cite: 23]

    # --- SECCIÓN 2: ANTECEDENTES PATOLÓGICOS (Checklist Pág. 1) ---
    vista = Column(Text, nullable=True) [cite: 25, 37]
    auditivo = Column(Text, nullable=True) [cite: 26, 38]
    respiratorios = Column(Text, nullable=True) [cite: 27, 39]
    cardiovasculares = Column(Text, nullable=True) [cite: 28, 40]
    estomago_intestino = Column(Text, nullable=True) [cite: 29, 42]
    sangre = Column(Text, nullable=True) [cite: 29, 43]
    genitourinario = Column(Text, nullable=True) [cite: 30, 44]
    sistema_nervioso = Column(Text, nullable=True) [cite: 31, 46]
    psiquiatricos_mentales = Column(Text, nullable=True) [cite: 32, 33]
    osteomusculares = Column(Text, nullable=True) [cite: 47, 49]
    endocrinos_metabolicos = Column(Text, nullable=True) [cite: 48, 50]
    reumatologicos = Column(Text, nullable=True) [cite: 52]
    dermatologicos = Column(Text, nullable=True) [cite: 56]
    generales_cancer_hernias = Column(Text, nullable=True) [cite: 53, 54]

    # --- ALERGIAS E INFECCIONES ---
    alergias_medicamentos = Column(Text, nullable=True) [cite: 58, 60]
    alergias_alimentos = Column(Text, nullable=True) [cite: 59, 60]
    infecciones_detalle = Column(Text, nullable=True) [cite: 61, 62] # Chagas, Hepatitis, etc.
    
    # --- ANTECEDENTES PERSONALES Y CIRUGÍAS (Pág. 2) ---
    cirugias = Column(Text, nullable=True) [cite: 63, 64]
    accidentes_trabajo = Column(Text, nullable=True) [cite: 65, 66]
    accidentes_particulares = Column(Text, nullable=True) [cite: 68, 69]
    medicamentos_uso_actual = Column(Text, nullable=True) [cite: 70, 71]
    grupo_sanguineo = Column(String, nullable=True) [cite: 73]
    deportes = Column(Text, nullable=True) [cite: 75, 76]
    
    # --- HÁBITOS ---
    alcohol = Column(String, nullable=True) [cite: 82]
    tabaco = Column(String, nullable=True) [cite: 83]
    drogas = Column(String, nullable=True) [cite: 84]
    coca_bolo = Column(String, nullable=True) [cite: 85, 86]
    
    # --- HISTORIA LABORAL Y RIESGOS ---
    edad_inicio_trabajo = Column(Integer, nullable=True) [cite: 90]
    historia_laboral_detalle = Column(Text, nullable=True) [cite: 88, 89] # Empresas, cargos, tiempos
    riesgos_expuestos = Column(Text, nullable=True) # Ruido, Radiación, Químicos, etc. [cite: 91, 92]
    uso_epp = Column(String, nullable=True) [cite: 90]

    # --- CIERRE ---
    observaciones = Column(Text, nullable=True) [cite: 120]
    
    paciente = relationship("Paciente", back_populates="declaraciones")
