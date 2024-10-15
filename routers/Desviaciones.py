from fastapi import APIRouter, HTTPException
from models.Desviaciones import Desviaciones, DesviacionesResponse, SeguimientoDesviacionResponse,SeguimientoDesviaciones,ResumenDesviaciones
from db.db import get_db
from typing import List,Dict
router = APIRouter(
    prefix="/desviaciones",
    tags=["Desviaciones"],
)



@router.get('/resumen', response_model=List[ResumenDesviaciones])
def get_resumen_desviaciones():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT 
                    d.Area,
                    COUNT(d.ID) AS desviaciones_detectadas,
                    d.Nivel,
                    SUM(CASE WHEN sd.Avance = '100' THEN 1 ELSE 0 END) AS desviaciones_corregidas,
                    (SUM(CASE WHEN sd.Avance = '100' THEN 1 ELSE 0 END) * 100.0) / COUNT(d.ID) AS porcentaje_corregidas
                FROM 
                    Desviaciones d
                LEFT JOIN 
                    SeguimientoDesviacion sd ON d.ID = sd.IDDesviacion
                GROUP BY 
                    d.Area, d.Nivel
            """)
            
            result = cursor.fetchall()
            
            # Estructura de almacenamiento para agrupar por área
            area_data: Dict[str, Dict] = {}

            for row in result:
                area = row[0]
                desviaciones_detectadas = int(row[1])
                nivel_riesgo = row[2].lower()  # Convertir a minúsculas para manejarlo mejor (bajo, medio, alto)
                desviaciones_corregidas = int(row[3])
                porcentaje_corregidas = float(row[4]) if row[4] is not None else 0.0

                # Si el área ya existe, actualizamos los valores sumando
                if area in area_data:
                    area_data[area]['desviaciones_detectadas'] += desviaciones_detectadas
                    area_data[area]['desviaciones_corregidas'] += desviaciones_corregidas
                    area_data[area]['riesgo'][nivel_riesgo] += desviaciones_detectadas  # Sumar desviaciones detectadas
                else:
                    # Si no existe, creamos una nueva entrada
                    area_data[area] = {
                        'desviaciones_detectadas': desviaciones_detectadas,
                        'desviaciones_corregidas': desviaciones_corregidas,
                        'riesgo': {
                            'bajo': 0,
                            'medio': 0,
                            'alto': 0
                        }
                    }
                    area_data[area]['riesgo'][nivel_riesgo] = desviaciones_detectadas  # Sumar desviaciones detectadas

            
            # Creamos la lista final con el resumen de cada área
            resumen_data = []
            for area, data in area_data.items():
                desviaciones_detectadas = data['desviaciones_detectadas']
                desviaciones_corregidas = data['desviaciones_corregidas']
                porcentaje_corregidas = (
                    (desviaciones_corregidas * 100.0) / desviaciones_detectadas
                    if desviaciones_detectadas > 0
                    else 0
                )
                estado_general = "Revisar"  # Esto es un placeholder, puedes añadir tu lógica aquí

                resumen = ResumenDesviaciones(
                    area=area,
                    desviaciones_detectadas=desviaciones_detectadas,
                    nivel_riesgo=data['riesgo'],  # Aquí incluimos el diccionario de riesgos
                    desviaciones_corregidas=desviaciones_corregidas,
                    porcentaje_corregidas=porcentaje_corregidas,
                    estado_general=estado_general
                )
                resumen_data.append(resumen)

            # Añadir una fila total
            total_desviaciones_detectadas = sum(res.desviaciones_detectadas for res in resumen_data)
            total_desviaciones_corregidas = sum(res.desviaciones_corregidas for res in resumen_data)
            porcentaje_total_corregidas = (
                (total_desviaciones_corregidas / total_desviaciones_detectadas * 100)
                if total_desviaciones_detectadas > 0
                else 0
            )
            
            # Calcular el total de cada nivel de riesgo
            total_riesgo = {
                'bajo': sum(res.nivel_riesgo['bajo'] for res in resumen_data),
                'medio': sum(res.nivel_riesgo['medio'] for res in resumen_data),
                'alto': sum(res.nivel_riesgo['alto'] for res in resumen_data)
            }

            
            return resumen_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener resumen de desviaciones: {str(e)}")

@router.get('/getDesviacion/{id}')
def get_seguimiento(id: int):
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute("""     
                           SELECT Deteccion,Seguimiento,Avance,Responsable ,Observacion FROM SeguimientoDesviacion WHERE  IDDesviacion=?
                           """,
                           (id,))
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
            return {
                "Deteccion": result[0],
                "Seguimiento": result[1],
                "Avance": result[2],
                "Responsable": result[3],
                "Observacion": result[4]
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener seguimiento: {str(e)}")
        
            


@router.put('/updateSeguimiento/{id}')
def update_seguimiento(desviacion: SeguimientoDesviaciones, id: int):
    try:
        with get_db() as connect:
            cursor = connect.cursor()

            # Verificar si el seguimiento ya existe
            cursor.execute('SELECT COUNT(*) FROM SeguimientoDesviacion WHERE IDDesviacion = ?', (id,))
            seguimiento_exists = cursor.fetchone()[0]

            if seguimiento_exists == 0:
                # Insertar un nuevo seguimiento si no existe
                cursor.execute(
                    '''
                    INSERT INTO SeguimientoDesviacion (IDDesviacion, Deteccion, Seguimiento, Avance, Responsable, Observacion) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        id,
                        desviacion.Deteccion,
                        desviacion.Seguimiento,
                        desviacion.Avance,
                        desviacion.Responsable,
                        desviacion.Observacion,
                    )
                )
                message = "Seguimiento agregado exitosamente"
            else:
                # Actualizar el seguimiento existente
                cursor.execute(
                    '''
                    UPDATE SeguimientoDesviacion 
                    SET Deteccion = ?, Seguimiento = ?, Avance = ?, Responsable = ?, Observacion = ? 
                    WHERE IDDesviacion = ?
                    ''',
                    (
                        desviacion.Deteccion,
                        desviacion.Seguimiento,
                        desviacion.Avance,
                        desviacion.Responsable,
                        desviacion.Observacion,
                        id
                    )
                )
                message = "Seguimiento actualizado exitosamente"
            
            connect.commit()

        return {"message": message}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar seguimiento: {str(e)}"
        )



@router.post('/addSeguimiento/{id}')
def addSeguimiento(desviacion: SeguimientoDesviaciones, id: int):
    try:
        with get_db() as connect:
            cursor = connect.cursor()

            # Verificar si la desviación existe antes de agregar seguimiento
            cursor.execute('SELECT COUNT(*) FROM Desviaciones WHERE ID = ?', (id,))
            if cursor.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="Desviación no encontrada")

            # Insertar seguimiento
            cursor.execute(
                '''
                INSERT INTO SeguimientoDesviacion (IDDesviacion, Deteccion, Seguimiento, Avance, Responsable, Observacion) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    id,
                    desviacion.Deteccion,
                    desviacion.Seguimiento,
                    desviacion.Avance,
                    desviacion.Responsable,
                    desviacion.Observacion
                )
            )
            connect.commit()

        return {"message": "Seguimiento agregado exitosamente"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al agregar seguimiento: {str(e)}"
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
