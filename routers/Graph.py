from fastapi import APIRouter
from fastapi.responses import JSONResponse
import plotly.graph_objs as go
import plotly.io as pio

router = APIRouter(
    prefix="/graph",
    tags=["Graph"],

)


@router.get('/get-graph-incendio')
def get_graph_incendio():
    data = [
        {
            "marker": {"color": "blue"},
            "name": "Planificadas",
            "x": [
                "EXTINTORES PORTÁTILES", "LÁMPARAS DE EMERGENCIA", 
                "INSPECCIÓN DE CAJETINES CON MANGUERAS", "INSPECCIÓN DE BOMBA CONTRA INCENDIOS", 
                "INSPECCIÓN DE PUERTAS Y ESCALERAS EXTERNAS", "TOTAL INSPECCIONES"
            ],
            "y": [6, 4, 12, 5, 4, 30],
            "type": "bar",
        },
        {
            "marker": {"color": "red"},
            "name": "Ejecutadas",
            "x": [
                "EXTINTORES PORTÁTILES", "LÁMPARAS DE EMERGENCIA", 
                "INSPECCIÓN DE CAJETINES CON MANGUERAS", "INSPECCIÓN DE BOMBA CONTRA INCENDIOS", 
                "INSPECCIÓN DE PUERTAS Y ESCALERAS EXTERNAS", "TOTAL INSPECCIONES"
            ],
            "y": [5, 3, 15, 5, 4, 33],
            "type": "bar",
        },
        {
            "marker": {"color": "green"},
            "mode": "lines+markers",
            "name": "% Cumplimiento",
            "x": [
                "EXTINTORES PORTÁTILES", "LÁMPARAS DE EMERGENCIA", 
                "INSPECCIÓN DE CAJETINES CON MANGUERAS", "INSPECCIÓN DE BOMBA CONTRA INCENDIOS", 
                "INSPECCIÓN DE PUERTAS Y ESCALERAS EXTERNAS", "TOTAL INSPECCIONES"
            ],
            "y": [83, 75, 125, 100, 100, 110],
            "yaxis": "y2",
            "type": "scatter",
        },
    ]

    layout = {
        "barmode": "group",
        "legend": {
            "x": 0.01,
            "y": 1.15,
            "orientation": "h",
            "font": {"size": 12, "family": "Arial, sans-serif"},  # Mejor fuente
            "bgcolor": "rgba(255, 255, 255, 0.5)",
            "bordercolor": "rgba(0, 0, 0, 0.3)",
            "borderwidth": 1,
        },
        "plot_bgcolor": "#f9f9f9",
        "paper_bgcolor": "#ffffff",
        "margin": {"l": 80, "r": 80, "b": 120, "t": 120, "pad": 10},
        "title": {
            "text": "Planificación vs Ejecución de Inspecciones y % Cumplimiento",
            "font": {"size": 22, "family": "Arial, sans-serif"},  # Texto más grande y fuente mejorada
            "x": 0.5,
            "xanchor": "center"
        },
        "xaxis": {
            "title": {
                "text": "Tipos de Inspecciones",
                "font": {"size": 16, "family": "Arial, sans-serif"},  # Mejora en el tamaño y fuente
            },
            "tickangle": -30,  # Ángulo más suave para mejor legibilidad
            "tickfont": {"size": 12, "family": "Arial, sans-serif"},  # Aumenta el tamaño de las etiquetas en el eje X
            "automargin": True
        },
        "yaxis": {
            "title": {
                "text": "Cantidad Planificadas/Ejecutadas",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            "tickfont": {"size": 12, "family": "Arial, sans-serif"}  # Fuente para los ticks del eje Y
        },
        "yaxis2": {
            "title": {
                "text": "% Cumplimiento",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            "tickfont": {"size": 12, "family": "Arial, sans-serif"},  # Fuente para los ticks del eje Y2
            "overlaying": "y",
            "side": "right",
        },
        "hovermode": "closest",
    }

    return JSONResponse(content={"data": data, "layout": layout})


@router.get("/get-graph-data")
def get_graph_data():

    data = [
        {
            "marker": {"color": "blue"},
            "name": "Planificadas",
            "x": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Total"],
            "y": [6, 4, 12, 5, 4, 5, 3, 4, 43],
            "type": "bar",
        },
        {
            "marker": {"color": "red"},
            "name": "Ejecutadas",
            "x": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Total"],
            "y": [5, 3, 15, 5, 4, 5, 3, 6, 46],
            "type": "bar",
        },
        {
            "marker": {"color": "green"},
            "mode": "lines+markers",
            "name": "% Cumplimiento",
            "x": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Total"],
            "y": [83, 75, 125, 100, 100, 100, 100, 150, 105],
            "yaxis": "y2",
            "type": "scatter",
        },
    ]

    layout = {
    "barmode": "group",
    "legend": {
        "x": 0.01,
        "y": 1.15,
        "orientation": "h",
        "font": {"size": 14, "family": "Arial, sans-serif"},
        "bgcolor": "rgba(255, 255, 255, 0.5)",
        "bordercolor": "rgba(0, 0, 0, 0.3)",
        "borderwidth": 1,
    },
    "plot_bgcolor": "#f9f9f9",
    "paper_bgcolor": "#ffffff",
    "margin": {"l": 80, "r": 80, "b": 150, "t": 120, "pad": 10},  # Aumenta margen inferior para etiquetas largas
    "title": {
        "text": "Planificación vs Ejecución de Inspecciones y % Cumplimiento",
        "font": {"size": 22, "family": "Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center"
    },
    "xaxis": {
        "title": {
            "text": "Tipos de Inspecciones",
            "font": {"size": 16, "family": "Arial, sans-serif"},
        },
        "tickvals": [
            "EXTINTORES PORTÁTILES", "LÁMPARAS DE EMERGENCIA", 
            "INSPECCIÓN DE CAJETINES CON MANGUERAS", "INSPECCIÓN DE BOMBA CONTRA INCENDIOS", 
            "INSPECCIÓN DE PUERTAS Y ESCALERAS EXTERNAS", "TOTAL INSPECCIONES"
        ],
        "ticktext": [
            "EXTINTORES\nPORTÁTILES", "LÁMPARAS\nDE EMERGENCIA", 
            "INSPECCIÓN\nDE CAJETINES\nCON MANGUERAS", "INSPECCIÓN\nDE BOMBA\nCONTRA INCENDIOS", 
            "INSPECCIÓN\nDE PUERTAS Y\nESCALERAS EXTERNAS", "TOTAL\nINSPECCIONES"
        ],
        "tickfont": {"size": 12, "family": "Arial, sans-serif"},
        "tickangle": 0,  # Forzar etiquetas horizontales
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


    return JSONResponse(content={"data": data, "layout": layout})
