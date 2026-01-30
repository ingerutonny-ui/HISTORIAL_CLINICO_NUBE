from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Cambiado a importación relativa para evitar errores en Render
import datetime
import random

class Paciente(Base):
    __tablename__ = "pacientes"

    # ID interno de la base de datos
    id = Column(Integer, primary_key=True, index=True)
    
    # --- DATOS DEL FORMULARIO INICIAL ---
    codigo_paciente = Column(String, unique=True, index=True) # Ejemplo: RA6855
    fecha_ingreso = Column(DateTime, default=datetime.datetime.now)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    documento_identidad = Column(String, unique=True, index=True)

    # --- DATOS DE AFILIACION ---
    edad = Column(Integer)
    sexo = Column(String)
    fecha_nacimiento = Column(Date)
    lugar_nacimiento = Column(String)
    domicilio_av_calle = Column(String)
    numero_domicilio = Column(String)
    barrio = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    telefono = Column(String)
    estado_civil = Column(String)
    profesion_labor = Column(String)

    # RELACIÓN: Un paciente puede tener muchas declaraciones juradas
    declaraciones = relationship("DeclaracionJurada", back_populates="paciente")

    def generar_codigo(self):
        """Genera el código tipo RA6855 usando iniciales y 4 números"""
        ini_n = self.nombres[0].upper() if self.nombres else "X"
        ini_a = self.apellidos[0].upper() if self.apellidos else "X"
        num_aleatorio = random.randint(1000, 9999)
        return f"{ini_n}{ini_a}{num_aleatorio}"


class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha_creacion = Column(DateTime, default=datetime.datetime.now)

    # 1. ANTECEDENTES PATOLÓGICOS (Basado en el PDF)
    enfermedad_vista = Column(Boolean, default=False)
    enfermedad_oido = Column(Boolean, default=False)
    enfermedad_respiratoria = Column(Boolean, default=False)
    enfermedad_cardiovascular = Column(Boolean, default=False)
    enfermedad_digestiva = Column(Boolean, default=False)
    enfermedad_genitourinaria = Column(Boolean, default=False)
    sistema_nervioso = Column(Boolean, default=False)
    psiquiatricos_mentales = Column(Boolean, default=False)
    observaciones_medicas = Column(String)

    # 2. CIRUGÍAS Y ACCIDENTES
    cirugias = Column(String)
    accidentes_trabajo = Column(String)
    accidentes_particulares = Column(String)

    # 3. MEDICAMENTOS Y OTROS
    medicamentos_actuales = Column(String)
    grupo_sanguineo = Column(String)
    deportes_frecuencia = Column(String)

    # 4. HÁBITOS (Pijchar/Bolo incluido)
    alcohol = Column(Boolean, default=False)
    tabaco = Column(Boolean, default=False)
    drogas = Column(Boolean, default=False)
    coca_pijchar = Column(Boolean, default=False)
    detalles_habitos = Column(String)

    # 5. RIESGOS EXPUESTOS DURANTE VIDA LABORAL
    riesgo_ruido = Column(Boolean, default=False)
    riesgo_radiacion = Column(Boolean, default=False)
    riesgo_quimico = Column(Boolean, default=False)
    riesgo_ergonomico = Column(Boolean, default=False)
    uso_epp = Column(Boolean, default=True)

    # RELACIÓN INVERSA: Esta declaración pertenece a un paciente
    paciente = relationship("Paciente", back_populates="declaraciones")
