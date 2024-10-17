from fastapi import APIRouter, HTTPException
from models.Incendios import Incendios, IncendiosResponse
from db.db import get_db
from typing import List
router = APIRouter(
    prefix="/incendios",
    tags=["Incendios"],
)


@router.put('/modifyIncendio/{id}')
def modifyIncendio(incendio : Incendios,id : int):
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'UPDATE SistemaIncendios SET Nombre = ?, Planificado = ?, Ejecutado = ? WHERE ID = ?',
                (incendio.Nombre, incendio.Planificado, incendio.Ejecutado, id)
            )
            connect.commit()

        return {"message": "Incendio modificado exitosamente"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al modificar incendio: {str(e)}")
    finally:

        connect.close()
        

@router.get('/getIncendios', response_model=List[IncendiosResponse])
def getIncendios():
    try:
        # Usar 'with' para manejar la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'SELECT ID, Nombre, Planificado, Ejecutado FROM SistemaIncendios'
            )
            rows = cursor.fetchall()  # Recuperar todas las filas

            # Crear una lista de objetos IncendiosResponse
            incendios = []
            for row in rows:
                # Convertir Planificado y Ejecutado a números para la división
                try:
                    planificado = float(row[2])  # Asegurarse que son números
                    ejecutado = float(row[3])

                    # Evitar la división por cero
                    porcentaje = (ejecutado / planificado * 100) if planificado != 0 else 0
                except ValueError:
                    porcentaje = 0  # Manejar posibles conversiones inválidas

                incendios.append(
                    IncendiosResponse(
                        IDIncendio=row[0],
                        Nombre=row[1],
                        Planificado=row[2],
                        Ejecutado=row[3],
                        Porcentaje=str(porcentaje)
                    )
                )
            
            return incendios  # Devolver la lista de incendios

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al obtener incendios: {str(e)}"
        )
    finally:
        connect.close()



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
