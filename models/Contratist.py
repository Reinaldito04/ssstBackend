from pydantic import BaseModel

class Contratist(BaseModel):
    RIF: str
    GerenciaContr: str
    NombreContr: str
    TelefonoContr: str 
    DireccionContr : str
    EmailContr: str
    
class ContratistResponse(Contratist):
    id: int
    