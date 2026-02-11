from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class PacienteCreate(BaseModel):
    model_config = ConfigDict(extra='allow')

class FiliacionCreate(BaseModel):
    # Definimos solo lo mínimo necesario y permitimos TODO lo demás
    paciente_id: Any = None
    model_config = ConfigDict(extra='allow')
