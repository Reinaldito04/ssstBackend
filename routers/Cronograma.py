from fastapi import APIRouter,HTTPException
from db.db import get_db
from models.Cronograma import Cronograma,CronogramaResponse

from collections import defaultdict
from datetime import datetime

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


@router.get('/getCronogramaByMonth')
def get_cronogramas_by_month():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT ID, Fecha, InpE, InpP, Observacion FROM Cronograma')
            results = cursor.fetchall()

            # Diccionario para agrupar por mes y sumar valores
            cronogramas_agrupados = defaultdict(lambda: {'InpE': 0, 'InpP': 0})

            for row in results:
                fecha_str = row[1]  # Obtener la fecha en formato 'YYYY-MM-DD'
                try:
                    # Convertir la fecha a un objeto datetime con el formato adecuado
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                    mes_anio = fecha.strftime("%Y-%m")  # Obtener año y mes como 'YYYY-MM'
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=f"Formato de fecha incorrecto: {fecha_str}")

                # Asegurarse de que InpE e InpP sean convertidos a enteros antes de sumarlos
                try:
                    inpE = int(row[2])
                    inpP = int(row[3])
                except ValueError:
                    raise HTTPException(status_code=400, detail="Los valores de InpE o InpP no son válidos")

                # Sumar los valores de InpE e InpP en el mes correspondiente
                cronogramas_agrupados[mes_anio]['InpE'] += inpE
                cronogramas_agrupados[mes_anio]['InpP'] += inpP

            # Formatear el resultado
            cronogramas_formateados = []
            for mes_anio, valores in cronogramas_agrupados.items():
                cronograma = {
                    'Mes': mes_anio,
                    'InpE_total': valores['InpE'],
                    'InpP_total': valores['InpP']
                }
                cronogramas_formateados.append(cronograma)

            return cronogramas_formateados

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los cronogramas: {str(e)}"
        )

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
    