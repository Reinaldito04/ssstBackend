from fastapi import APIRouter, HTTPException
from db.db import get_db
from models.Contratist import Contratist, ContratistResponse, ControlContratista, ControlContratistaResponse, ContratistaMinimalResponse
from typing import List, Optional
import sqlite3

router = APIRouter(
    prefix="/contratistas",
    tags=["Contratistas"],
)


@router.get("/graficaContratistas")
def grafica_contratistas():
    conn = get_db()
    cursor = conn.cursor()

    # Consulta para agrupar por mes y año, sumando planificadas y ejecutadas
    cursor.execute("""
        SELECT 
            strftime('%Y-%m', cc.FechaInicio) AS MesAnio,  -- Agrupando por año y mes (YYYY-MM)
            SUM(cc.Planificado) AS TotalPlanificado,      -- Suma de horas planificadas
            SUM(cc.Ejecutado) AS TotalEjecutado           -- Suma de horas ejecutadas
        FROM 
            ControlContratistas cc
        INNER JOIN
            Contratistas c ON c.ID = cc.IDContratistas
        GROUP BY 
            strftime('%Y-%m', cc.FechaInicio)             -- Agrupación por mes y año
        ORDER BY 
            MesAnio ASC                                   -- Ordenar de forma ascendente
    """)

    rows = cursor.fetchall()

    # Convertir los resultados a un formato legible
    resultado = [
        {
            "Mes": row[0],  # Mes y año en formato YYYY-MM
            "TotalPlanificado": row[1],  # Suma de horas planificadas
            "TotalEjecutado": row[2],  # Suma de horas ejecutadas
            "Cumplimiento": (row[2] / row[1]) * 100 if row[1] > 0 else 0  # Calcular el porcentaje
        }
        for row in rows
    ]

    conn.close()

    return resultado

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
