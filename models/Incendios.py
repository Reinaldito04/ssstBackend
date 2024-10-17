from pydantic import BaseModel
from typing import Optional

class Incendios(BaseModel):
    Nombre : str 
    Planificado :str
    Ejecutado :str
    
class IncendiosResponse(Incendios):
    IDIncendio: int