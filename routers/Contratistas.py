from fastapi import APIRouter, HTTPException
from db.db import get_db
from models.Contratist import Contratist,ContratistResponse
from typing import List


router = APIRouter(
    prefix="/contratistas",
    tags=["Contratistas"],
)


@router.get("/all", response_model=List[ContratistResponse])
def get_contratists():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT RIF, GerenciaContr, NombreContr, TelefonoContr, DireccionContr, EmailContr,ID FROM Contratistas")
            result = cursor.fetchall()
            
            # Convertir los resultados a una lista de diccionarios
            contratists = [
                {
                    "id" : row[6],
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
        raise HTTPException(status_code=500, detail=f"Error al visualizar contratistas: {str(e)}")

    
@router.post('/addContratist')
def agg_Contrati(contratist: Contratist):
    try:
        # Usar 'with' para manejar la conexión a la base de datos
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute(
                'INSERT INTO Contratistas (RIF, GerenciaContr, NombreContr, TelefonoContr, DireccionContr, CorreoContr) VALUES (?, ?, ?, ?, ?, ?)',
                (contratist.RIF, contratist.GerenciaContr, contratist.NombreContr, contratist.TelefonoContr, contratist.DireccionContr, contratist.EmailContr)
            )
            connect.commit()
        
        # Retornar un mensaje de éxito
        return {"message": "Contratista agregado exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(status_code=500, detail=f"Error al agregar contratista: {str(e)}")

    
