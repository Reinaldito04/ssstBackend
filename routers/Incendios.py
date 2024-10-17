from fastapi import APIRouter,HTTPException
from models.Incendios import Incendios
from db.db import get_db
router = APIRouter(
    prefix="/incendios",
    tags=["Incendios"],
)

@router.post('/addIncendio')
def addIncendio(incendio: Incendios):
    try:
        # Usar 'with' para manejar la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'INSERT INTO SistemaIncendios (Nombre, Planificado, Ejecutado) VALUES (?, ?, ?)',
                (incendio.Nombre, incendio.Planificado, incendio.Ejecutado)
            )
            connect.commit()

        # Retornar un mensaje de éxito
        return {"message": "Incendio agregado exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al agregar incendio: {str(e)}")
    finally:
        
        connect.close()
