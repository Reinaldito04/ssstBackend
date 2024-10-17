from fastapi import APIRouter, HTTPException
from db.db import get_db
from models.Contratist import Contratist, ContratistResponse, ControlContratista, ControlContratistaResponse, ContratistaMinimalResponse
from typing import List, Optional
import sqlite3

router = APIRouter(
    prefix="/contratistas",
    tags=["Contratistas"],
)


@router.get("/rendimiento", response_model=List[dict])
def get_rendimiento_contratista():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            cc.Planificado,    -- Horas planificadas
            cc.Ejecutado,      -- Horas ejecutadas
            cc.EvalFinal,      -- Evaluación final
            c.NombreContr
        FROM 
            ControlContratistas cc
        INNER JOIN 
            Contratistas c
        ON
            cc.IDContratistas = c.ID
        """
    )

    rendimiento = cursor.fetchall()

    if not rendimiento:
        raise HTTPException(status_code=404, detail="Contratista no encontrado o sin datos de rendimiento")

    # Convertir el resultado en un formato de respuesta legible
    rendimiento_data = []
    for row in rendimiento:
        planificado = int(row[0]) if row[0] is not None else 0
        ejecutado = int(row[1]) if row[1] is not None else 0
        cumplimiento = (ejecutado / planificado) * 100 if planificado > 0 else 0

        rendimiento_data.append({
            "Planificado": planificado,
            "Ejecutado": ejecutado,
            "Cumplimiento": cumplimiento,
            "EvalFinal": row[2],  # EvalFinal está en la posición 2
            "Contratista": row[3] # NombreContr está en la posición 3
        })

    return rendimiento_data


@router.get('/seguimientoContratist/{idContratist}')
def get_contratist(idContratist: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            c.ID,               -- ID from Contratistas
            c.NombreContr,    
            cc.AnexoA,      
            cc.AnexoB,    
            cc.PDTART,
            cc.Planificado,
            cc.Ejecutado,
            cc.Cumplimiento,
            cc.EvalFinal
        FROM 
            Contratistas c
        INNER JOIN
            ControlContratistas cc ON c.ID = cc.IDContratistas
        WHERE c.ID = ?
        """,
        (idContratist,)  # Pasamos idContratist como una tupla
    )
    
    contratistas = cursor.fetchall()

    # Convertir los resultados a una lista de diccionarios
    contratists = [
        {
            "id": row[0],
            "Nombre": row[1],
            "AnexoA": row[2],
            "AnexoB": row[3],
            "PDTART": row[4],
            "Planificado": row[5],
            "Ejecutado": row[6],
            "Cumplimiento": row[7],
            "EvalFinal": row[8]
        }
        for row in contratistas
    ]

    return contratists

    
    

  
        
        


            


@router.get('/consultContratist')
def get_contratist():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            c.ID,               -- ID from Contratistas
            c.RIF,              -- RIF from Contratistas
            c.NombreContr,      -- Nombre from Contratistas
            c.GerenciaContr,    -- Gerencia from Contratistas
            cc.NContrato,
            cc.FechaInicio,
            cc.FechaFin
        FROM 
            Contratistas c
        INNER JOIN
            ControlContratistas cc ON c.ID = cc.IDContratistas
        """
    )
    contratistas = cursor.fetchall()

    # Convertir los resultados a una lista de diccionarios
    contratists = [
        {
            "id": row[0],
            "RIF": row[1],
            "NombreContr": row[2],
            "GerenciaContr": row[3],
            "NContrato": row[4],
            "FechaInicio": row[5],
            "FechaFin": row[6],
        }
        for row in contratistas
    ]

    return contratists



@router.get('/getControl/{idContratista}')
def get_contratista(idContratista: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            cc.ID,               -- ID from ControlContratistas
            cc.NContrato,
            cc.Planificado,
            cc.Ejecutado,
            cc.Cumplimiento,
            cc.ServicioEvaluar,
            cc.FechaInicio,
            cc.FechaFin,
            cc.Eval1,
            cc.Eval2,
            cc.Eval3,
            cc.Eval4,
            cc.PromD,
            cc.EvalFinal,
            cc.PDTART,
            cc.Observaciones,
            cc.AnexoA,
            cc.AnexoB,
            c.ID AS Contratista, -- ID from Contratistas
            c.NombreContr,       -- Nombre del Contratista
            c.GerenciaContr      -- Gerencia del Contratista
        FROM 
            ControlContratistas cc
        INNER JOIN 
            Contratistas c ON cc.IDContratistas = c.ID
        WHERE 
            c.ID = ?
        """, (idContratista,)
    )

    contratista = cursor.fetchone()

    if contratista is None:
        # Si no se encuentra el contratista en ControlContratistas, obtener solo el nombre y la gerencia
        cursor.execute(
            """
            SELECT 
                c.NombreContr, 
                c.GerenciaContr
            FROM 
                Contratistas c
            WHERE 
                c.ID = ?
            """, (idContratista,)
        )
        minimal_contratista = cursor.fetchone()

        if minimal_contratista is None:
            raise HTTPException(
                status_code=404, detail="Contratista no encontrado")

        # Retornar solo nombre y gerencia
        return ContratistaMinimalResponse(
            NombreContr=minimal_contratista[0],
            GerenciaContr=minimal_contratista[1]
        )
    else:
        # Retornar un diccionario con todos los datos
        return ControlContratistaResponse(
            ID=contratista[0],
            NContrato=contratista[1],
            Planificado=contratista[2],
            Ejecutado=contratista[3],
            Cumplimiento=contratista[4],
            ServicioEvaluar=contratista[5],
            FechaInicio=contratista[6],
            FechaFin=contratista[7],
            Eval1=contratista[8],
            Eval2=contratista[9],
            Eval3=contratista[10],
            Eval4=contratista[11],
            PromD=contratista[12],
            EvalFinal=contratista[13],
            PDTART=contratista[14],
            Observaciones=contratista[15],
            AnexoA=contratista[16],
            AnexoB=contratista[17],
            Contratista=contratista[18],  # ID del contratista
            NombreContr=contratista[19],   # Nombre del contratista
            GerenciaContr=contratista[20]   # Gerencia del contratista
        )


@router.put('/controlContratista/{idContratista}', response_model=ControlContratista)
def control_contratista(idContratista: int, contratista: ControlContratista):
    conn = get_db()
    cursor = conn.cursor()

    # Verifica si el IDContratistas ya existe
    cursor.execute(
        "SELECT * FROM ControlContratistas WHERE IDContratistas = ?", (idContratista,))
    existing_contratista = cursor.fetchone()

    if existing_contratista:
        # Actualiza el registro existente
        cursor.execute("""
            UPDATE ControlContratistas 
            SET NContrato = ?, Planificado = ?, Ejecutado = ?, Cumplimiento = ?, 
                ServicioEvaluar = ?, FechaInicio = ?, FechaFin = ?, Eval1 = ?, 
                Eval2 = ?, Eval3 = ?, Eval4 = ?, PromD = ?, EvalFinal = ?, 
                PDTART = ?, Observaciones = ?, AnexoA = ?, AnexoB = ?
            WHERE IDContratistas = ?
        """, (
            contratista.NContrato, contratista.Planificado, contratista.Ejecutado,
            contratista.Cumplimiento, contratista.ServicioEvaluar, contratista.FechaInicio,
            contratista.FechaFin, contratista.Eval1, contratista.Eval2,
            contratista.Eval3, contratista.Eval4, contratista.PromD,
            contratista.EvalFinal, contratista.PDTART, contratista.Observaciones,
            contratista.AnexoA, contratista.AnexoB, idContratista
        ))
        conn.commit()
        conn.close()
        return contratista

    else:
        # Inserta el nuevo registro
        try:
            cursor.execute("""
                INSERT INTO ControlContratistas (IDContratistas, NContrato, Planificado, Ejecutado, Cumplimiento, 
                                                   ServicioEvaluar, FechaInicio, FechaFin, Eval1, Eval2, Eval3, 
                                                   Eval4, PromD, EvalFinal, PDTART, Observaciones, AnexoA, AnexoB)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                idContratista, contratista.NContrato, contratista.Planificado, contratista.Ejecutado,
                contratista.Cumplimiento, contratista.ServicioEvaluar, contratista.FechaInicio,
                contratista.FechaFin, contratista.Eval1, contratista.Eval2,
                contratista.Eval3, contratista.Eval4, contratista.PromD,
                contratista.EvalFinal, contratista.PDTART, contratista.Observaciones,
                contratista.AnexoA, contratista.AnexoB
            ))
            conn.commit()
            conn.close()
            return contratista
        except sqlite3.IntegrityError:
            conn.close()
            raise HTTPException(
                status_code=400, detail="IDContratistas ya existe. Inserción fallida.")


@router.get("/all", response_model=List[ContratistResponse])
def get_contratists():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                "SELECT RIF, GerenciaContr, NombreContr, TelefonoContr, DireccionContr, EmailContr,ID FROM Contratistas")
            result = cursor.fetchall()

            # Convertir los resultados a una lista de diccionarios
            contratists = [
                {
                    "id": row[6],
                    "RIF": row[0],
                    "GerenciaContr": row[1],
                    "NombreContr": row[2],
                    "TelefonoContr": row[3],
                    "DireccionContr": row[4],
                    "EmailContr": row[5],


                }
                for row in result
            ]
            return contratists
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al visualizar contratistas: {str(e)}")


@router.post('/addContratist')
def agg_Contrati(contratist: Contratist):
    try:
        # Usar 'with' para manejar la conexión a la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'INSERT INTO Contratistas (RIF, GerenciaContr, NombreContr, TelefonoContr, DireccionContr, EmailContr) VALUES (?, ?, ?, ?, ?, ?)',
                (contratist.RIF, contratist.GerenciaContr, contratist.NombreContr,
                 contratist.TelefonoContr, contratist.DireccionContr, contratist.EmailContr)
            )
            connect.commit()

        # Retornar un mensaje de éxito
        return {"message": "Contratista agregado exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500, detail=f"Error al agregar contratista: {str(e)}")
