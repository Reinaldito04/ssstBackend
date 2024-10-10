from fastapi import APIRouter, File, UploadFile, HTTPException,Form
import json
import shutil
from models.Capacitacion import Capacitacion,CapacitacionResponse
from db.db import get_db
from fastapi.responses import JSONResponse
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import datetime

router = APIRouter(
    prefix="/capacitacion",
    tags=["Capacitacion"],
)


def get_data_from_db():
    # Aquí deberías realizar la conexión a tu base de datos SQLite
    # y ejecutar la consulta para obtener las horas planificadas y ejecutadas.
    # Este es un ejemplo básico. Modifícalo según tu esquema de base de datos.
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
    SELECT strftime('%Y-%m', Fecha) AS mes,
           SUM(HP) AS hp,
           SUM(HE) AS he
    FROM Capacitacion
    GROUP BY mes
    ORDER BY mes;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    conn.close()
    
    # Convertir los datos en un diccionario
    data = {row[0]: {"hp": row[1], "he": row[2]} for row in rows}
    return data

@router.get("/getGraph")
async def get_graph():
    # Obtener los datos de la base de datos
    data = get_data_from_db()

    # Asumiendo que `data` es un diccionario con los meses como claves
    months = list(data.keys())
    hp_values = [int(data[month]["hp"]) for month in months]  # Convertir a int
    he_values = [int(data[month]["he"]) for month in months]  # Convertir a int

    # Calcular los totales
    totalHp = sum(hp_values)
    totalHe = sum(he_values)

    # Organizar los datos para la gráfica
    bar_data = [
        {
            "marker": {"color": "red"},
            "name": "Horas Planificadas (HP)",
            "x": months + ["Total"],
            "y": hp_values + [totalHp],
            "type": "bar",
        },
        {
            "marker": {"color": "blue"},
            "name": "Horas Ejecutadas (HE)",
            "x": months + ["Total"],
            "y": he_values + [totalHe],
            "type": "bar",
        },
        {
            "marker": {"color": "green"},
            "mode": "lines+markers",
            "name": "% Cumplimiento",
            "x": months + ["Total"],
            "y": [(he / hp) * 100 if hp != 0 else 0 for hp, he in zip(hp_values + [totalHp], he_values + [totalHe])],
            
            "type": "bar",
        },
    ]

    # Crear el layout de la gráfica
    layout = {
        "barmode": "group",
        "legend": {
            "x": 0.01,
            "y": 1.15,
            "orientation": "h",
            "font": {"size": 12, "family": "Arial, sans-serif"},
            "bgcolor": "rgba(255, 255, 255, 0.5)",
            "bordercolor": "rgba(0, 0, 0, 0.3)",
            "borderwidth": 1,
        },
        "plot_bgcolor": "#f9f9f9",
        "paper_bgcolor": "#ffffff",
        "margin": {"l": 80, "r": 80, "b": 120, "t": 120, "pad": 10},
        "title": {
            "text": "Planificación vs Ejecución de Horas y % Cumplimiento",
            "font": {"size": 22, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center"
        },
        "xaxis": {
            "title": {
                "text": "Meses",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            "tickangle": -30,
            "tickfont": {"size": 12, "family": "Arial, sans-serif"},
            "automargin": True
        },
        "yaxis": {
            "title": {
                "text": "Cantidad Planificadas/Ejecutadas",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            "tickfont": {"size": 12, "family": "Arial, sans-serif"}
        },
        "yaxis2": {
            "title": {
                "text": "% Cumplimiento",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            "tickfont": {"size": 12, "family": "Arial, sans-serif"},
            "overlaying": "y",
            "side": "right",
        },
        "hovermode": "closest",
    }

    return JSONResponse(content={"data": bar_data, "layout": layout})




@router.get('/getCapacitacion')
async def getCapacitacion():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Fecha, Tema, Objetivo, Expositor, Participantes, Hp, He, Archivo FROM Capacitacion")
    result = cursor.fetchall()
    
    capacitaciones = []  # Crear una lista para almacenar los resultados
    
    for row in result:
        capacitacion = CapacitacionResponse(
            id=row[0],
            Fecha=row[1],
            Tema=row[2],
            Objetivo=row[3],
            Expositor=row[4],
            participantes=row[5],
            HP=row[6],
            HE=row[7],
            Archivo=row[8]
        )
        capacitaciones.append(capacitacion)  # Agregar cada objeto a la lista
    
    return capacitaciones  # Devolver la lista de capacitaciones
  
@router.put('/modifyCapacitacion/{id}')
async def modifyCapacitacion(
    id:int,
    capacitacion: str = Form(...),  # Recibe el JSON como string desde FormData
    archivo: UploadFile = File(...)
):
    # Deserializar el JSON
    capacitacion_data = json.loads(capacitacion)
    capacitacion_obj = Capacitacion(**capacitacion_data)  # Crea el objeto usando Pydantic para validación

    # Definir la ruta donde se guardará el archivo
    file_location = f"File/{archivo.filename}"
    # Guardar el archivo en la ruta definida
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE Capacitacion
                   SET Fecha = ?, Tema = ?, Objetivo = ?, Expositor = ?, Participantes = ?, HP = ?, HE = ?, Archivo = ?
                   WHERE ID = ?
                   """, (
        
                       capacitacion_obj.Fecha,
                       capacitacion_obj.Tema,
                       capacitacion_obj.Objetivo,
                       capacitacion_obj.Expositor,
                       capacitacion_obj.participantes,
                       capacitacion_obj.HP,
                       capacitacion_obj.HE,
                       archivo.filename,
                       id
                       ))

    conn.commit()
    return ({"message": "Capacitación modificada"})

    
@router.get('/getCapacitacion/{id}')
async def getCapacion(id:int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Fecha, Tema, Objetivo, Expositor, Participantes, Hp, He, Archivo FROM Capacitacion WHERE ID = ?", (id,))
    result = cursor.fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Capacitación no encontrada")
    
    capacitacion = CapacitacionResponse(
        id=result[0],
        Fecha=result[1],
        Tema=result[2],
        Objetivo=result[3],
        Expositor=result[4],
        participantes=result[5],
        HP=result[6],
        HE=result[7],
        Archivo=result[8]
    )
    
    return capacitacion
    


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