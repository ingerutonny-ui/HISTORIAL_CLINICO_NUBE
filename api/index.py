from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from pydantic import BaseModel

# 1. Configuración de Base de Datos (Ruta permitida en Vercel)
SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Modelo de Base de Datos
class PacienteDB(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    dni = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# 3. Esquemas de validación (Pydantic)
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    dni: str

class Paciente(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# 4. Aplicación FastAPI
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
@app.get("/api/")
def read_root():
    return {"message": "API de Historial Clínico en la Nube funcionando"}

@app.get("/api/pacientes", response_model=List[Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(PacienteDB).all()
