from sqlalchemy import Column, Integer, String, Date, DateTime
from api.database import Base
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

    # --- DATOS DE AFILIACION (Resto de la tabla) ---
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

    def generar_codigo(self):
        """Genera el código tipo RA6855 usando iniciales y 4 números"""
        ini_n = self.nombres[0].upper() if self.nombres else "X"
        ini_a = self.apellidos[0].upper() if self.apellidos else "X"
        num_aleatorio = random.randint(1000, 9999)
        return f"{ini_n}{ini_a}{num_aleatorio}"
