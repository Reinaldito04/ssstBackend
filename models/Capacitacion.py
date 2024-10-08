from pydantic import BaseModel
from typing import Optional
from datetime import date

class Capacitacion(BaseModel):
    Fecha : Optional[str]
    Tema :Optional [str] 
    Objetivo :Optional [ str]
    Expositor:Optional [ str] 
    participantes : Optional [str ] 
    HP: Optional [str] 
    HE : Optional [str] 
     
    