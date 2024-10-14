from pydantic import BaseModel
from typing import Optional,List,Dict
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
    Deteccion: Optional[str]
    Seguimiento: Optional[str]
    Avance: Optional[str]
    Responsable: Optional[str]
    Observacion: Optional[str]
    
class SeguimientoDesviacionResponse(SeguimientoDesviaciones):
    IDDesviacion: int 
    ID: Optional[int]  # El campo ID ahora es opcional
    Descripcion: Optional[str]
    Area: Optional[str]
    

class ResumenDesviaciones(BaseModel):
    area: str
    desviaciones_detectadas: int
    desviaciones_corregidas: int
    porcentaje_corregidas: float
    nivel_riesgo: Dict[str, int]  # Cambiar de str a Dict para aceptar el formato {'bajo': X, 'medio': X, 'alto': X}
    estado_general: str