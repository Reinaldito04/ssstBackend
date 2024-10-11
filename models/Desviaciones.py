from pydantic import BaseModel
from typing import Optional
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
    
class DesviacionesResponse(Desviaciones):
    ID: int
    
class SeguimientoDesviaciones(BaseModel):
    IDDesviacion: int 
    Deteccion: Optional[str]
    Seguimiento: Optional[str]
    Avance: Optional[str]
    Responsable: Optional[str]
    Observacion: Optional[str]
    
class SeguimientoDesviacionResponse(SeguimientoDesviaciones):
    ID: Optional[int]  # El campo ID ahora es opcional
    Descripcion: Optional[str]
    Area: Optional[str]