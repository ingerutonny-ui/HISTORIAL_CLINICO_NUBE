from pydantic import BaseModel

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    ci: str
    fechaIngreso: str
    codigo: str

class PacienteResponse(PacienteBase):
    id: int

    class Config:
        orm_mode = True
