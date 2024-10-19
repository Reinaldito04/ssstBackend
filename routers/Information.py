from fastapi import APIRouter,HTTPException
from db.db import get_db
router = APIRouter(
    prefix="/information",
    tags=["Information"],
)

@router.get("/getAdministradoresCantidad")
def getAdministradoresCantidad():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT COUNT(*) FROM Users WHERE TypeUser = "Administrador"')
            count = cursor.fetchone()[0]  # Obtener el primer elemento del resultado
            return {"cantidad": count}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener la cantidad de administradores: {str(e)}"
        )
@router.get('/getAnalistasCantidad')
def getAnalistas():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT COUNT(*) FROM Users WHERE TypeUser = "Analista"')
            count = cursor.fetchone()[0]  # Obtener el primer elemento del resultado
            return {"cantidad": count}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener la cantidad de analistas: {str(e)}"
        )
        
@router.get('/getDesviacionesCantidad')
def getDesviacicones():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT COUNT(*) FROM Desviaciones')
            count = cursor.fetchone()[0]  # Obtener el primer elemento del resultado
            return {"cantidad": count}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener la cantidad de desviaciones: {str(e)}"
        )
        