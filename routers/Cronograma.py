from fastapi import APIRouter,HTTPException
from db.db import get_db
from models.Cronograma import Cronograma,CronogramaResponse
router = APIRouter(
    prefix="/cronograma",
    tags=["Cronograma"],
)

@router.get('/getCronograma/{id}')
def getCronograma(id : int):
    try :
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT ID,Fecha,InpE,inpP,Observacion  FROM Cronograma WHERE ID = ?', (id,))
            result = cursor.fetchone()
            cronograma = CronogramaResponse(
                ID=result[0],
                Fecha=result[1],
                InpE=result[2],
                InpP=result[3],
                Observacion=result[4]
            )
            return cronograma
    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al obtener cronograma: {str(e)}")

@router.put('/modifyCronograma/{id}')
def modifyCronograma(id: int, cronograma: Cronograma):
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            # Verificar si el cronograma existe antes de actualizarlo
            cursor.execute('SELECT ID FROM Cronograma WHERE ID = ?', (id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Cronograma no encontrado")

            # Actualizar los campos del cronograma
            cursor.execute('''
                UPDATE Cronograma 
                SET Fecha = ?, InpE = ?, InpP = ?, Observacion = ? 
                WHERE ID = ?
            ''', (cronograma.Fecha, cronograma.InpE, cronograma.InpP, cronograma.Observacion, id))

            connect.commit()

        return {"message": "Cronograma modificado exitosamente"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al modificar cronograma: {str(e)}")
@router.get('/getCronograma')
def getCronograma():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT ID,Fecha,InpE,inpP,Observacion  FROM Cronograma')
            result = cursor.fetchall()
            cronogramas = []
            for row in result :
                cronograma = CronogramaResponse(
                    ID=row[0],
                    Fecha=row[1],
                    InpE=row[2],
                    InpP=row[3],
                    Observacion=row[4]
                )
                cronogramas.append(cronograma)
            return cronogramas
            
          
          
          
    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al obtener cronograma: {str(e)}")

@router.post('/addCronograma')
def addCronograma(cronograma: Cronograma):
    try:
        # Usar 'with' para manejar laisclosed a la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'INSERT INTO Cronograma (Fecha, InpE, inpP, Observacion) VALUES (?, ?, ?, ?)',
                (cronograma.Fecha, cronograma.InpE, cronograma.InpP, cronograma.Observacion)
            )
            connect.commit()

        # Retornar un mensaje de₁xito
        return {"message": "Cronograma agregado exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al agregar cronograma: {str(e)}")
    