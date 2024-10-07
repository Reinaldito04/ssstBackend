from pydantic import BaseModel
from typing import Optional
from datetime import date
class Contratist(BaseModel):
    RIF: str
    GerenciaContr: str
    NombreContr: str
    TelefonoContr: str 
    DireccionContr : str
    EmailContr: str
    
class ContratistResponse(Contratist):
    id: int

class ControlContratista(BaseModel):
    NContrato: str
    Planificado: Optional[str] = None
    Ejecutado: Optional[str] = None
    Cumplimiento: Optional[str] = None
    ServicioEvaluar: Optional[str] = None
    FechaInicio: Optional[date]=None
    FechaFin: Optional[date]=None
    Eval1: Optional[str] = None
    Eval2: Optional[str] = None
    Eval3: Optional[str] = None
    Eval4: Optional[str] = None
    PromD: Optional[str] = None  
    EvalFinal: Optional[str] = None  
    PDTART: Optional[str] = None
    Observaciones: Optional[str] = None
    AnexoA: Optional[str] = None
    AnexoB: Optional[str] = None

class ControlContratistaResponse(ControlContratista):
    ID: int
    Contratista: int
    NombreContr :str
    GerenciaContr: str
    
class ContratistaMinimalResponse(BaseModel):
    NombreContr: str
    GerenciaContr: str