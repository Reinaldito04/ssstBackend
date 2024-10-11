from fastapi import APIRouter, HTTPException
from models.Desviaciones import Desviaciones, DesviacionesResponse, SeguimientoDesviacionResponse
from db.db import get_db

router = APIRouter(
    prefix="/desviaciones",
    tags=["Desviaciones"],
)


@router.get('/getSeguimiento')
def getSeguimiento():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute("""     
                           SELECT 
                            d.ID AS ID,
                            d.Descripcion AS Descripcion,
                            d.Area AS Area,
                            s.Deteccion AS Deteccion,
                            s.Seguimiento AS Seguimiento,
                            s.Avance,
                            s.Responsable,
                            s.Observacion,
                            s.ID
                        FROM 
                            Desviaciones d
                        LEFT JOIN 
                            SeguimientoDesviacion s
                        ON 
                            d.ID = s.IDDesviacion;
                           """)
            result = cursor.fetchall()
            seguimiento = []
            for row in result:
                 seguimiento.append(SeguimientoDesviacionResponse(
                    IDDesviacion=row[0],
                    Descripcion=row[1],
                    Area=row[2],
                    Deteccion=row[3],
                    Seguimiento=row[4],
                    Avance=row[5] if row[5] is not None else None,
                    Responsable=row[6] if row[6] is not None else None,
                    Observacion=row[7] if row[7] is not None else None,
                    ID=row[8] if row[8] is not None else None  # Manejar NULL en el campo ID
                ))
            return seguimiento
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener seguimiento: {str(e)}")


@router.get('/getDesviaciones')
def getDesviaciones():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'SELECT ID, Descripcion, Area, CausaRaiz, TipoInspeccion, Severidad, Frecuencia, Nivel, AccionesCorrectivas, Deteccion FROM Desviaciones')
            result = cursor.fetchall()
            desviaciones = []
            for row in result:
                desviaciones.append(DesviacionesResponse(
                    ID=row[0],
                    Descripcion=row[1],
                    Area=row[2],
                    CausaRaiz=row[3],
                    TipoInspeccion=row[4],
                    Severidad=row[5],
                    Frecuencia=row[6],
                    Nivel=row[7],
                    AccionesCorrectivas=row[8],
                    Deteccion=row[9]
                ))
            return desviaciones
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener desviaciones: {str(e)}")


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
