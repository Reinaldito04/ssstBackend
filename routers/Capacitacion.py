from fastapi import APIRouter, File, UploadFile, HTTPException,Form
import json
import shutil
from models.Capacitacion import Capacitacion
from db.db import get_db
router = APIRouter(
    prefix="/capacitacion",
    tags=["Capacitacion"],
)


@router.post('/addCapacitacion')
async def addCapacitacion(
    capacitacion: str = Form(...),  # Recibe el JSON como string desde FormData
    archivo: UploadFile = File(...)
):
    # Deserializar el JSON
    capacitacion_data = json.loads(capacitacion)
    capacitacion_obj = Capacitacion(**capacitacion_data)  # Crea el objeto usando Pydantic para validación

    # Definir la ruta donde se guardará el archivo
    file_location = f"File/{archivo.filename}"

    # Guardar el archivo
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(archivo.file, file_object)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO Capacitacion (Fecha, Tema, Objetivo, Expositor, Participantes, HP, HE, Archivo) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   """, (
                       capacitacion_obj.Fecha,
                       capacitacion_obj.Tema,
                       capacitacion_obj.Objetivo,
                       capacitacion_obj.Expositor,
                       capacitacion_obj.participantes,
                       capacitacion_obj.HP,
                       capacitacion_obj.HE,
                       archivo.filename
                   ))
    conn.commit()
    conn.close()
    
    return {"message": "Capacitación añadida correctamente", "archivo": archivo.filename,"capacitacion":capacitacion_obj}