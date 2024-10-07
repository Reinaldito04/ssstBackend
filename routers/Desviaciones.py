from fastapi import APIRouter,HTTPException
from models.Desviaciones import Desviaciones
from db.db import get_db

router = APIRouter(
    prefix="/desviaciones",
    tags=["Desviaciones"],
)
@router.post('/addDesviacion')
def addDesviacion(desviacion: Desviaciones):
    try:
        # Usar 'with' para manejar la conexión a la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'INSERT INTO Desviaciones (Descripcion, Area, CausaRaiz, TipoInspeccion, Severidad, Frecuencia, Nivel, AccionesCorrectivas, Deteccion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (desviacion.Descripcion, desviacion.Area, desviacion.CausaRaiz, desviacion.TipoInspeccion,
                 desviacion.Severidad, desviacion.Frecuencia, desviacion.Nivel, desviacion.AccionesCorrectivas,
                 desviacion.Deteccion)
            )
            connect.commit()

        # Retornar un mensaje de إxito
        return {"message": "Desviacion agregada exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al agregar desviacion: {str(e)}")
        

