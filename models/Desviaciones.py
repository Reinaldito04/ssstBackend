from pydantic import BaseModel

class Desviaciones(BaseModel):
    Descripcion: str
    Area : str 
    CausaRaiz : str 
    TipoInspeccion : str 
    Severidad : str
    Frecuencia : str 
    Nivel: str 
    AccionesCorrectivas : str 
    Deteccion : str