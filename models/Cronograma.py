from pydantic import BaseModel

class Cronograma(BaseModel):
    Fecha: str
    InpE: str 
    InpP : str 
    Observacion : str
   
class CronogramaResponse(Cronograma):
    ID: int