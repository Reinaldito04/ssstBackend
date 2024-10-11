from fastapi import FastAPI
import plotly.graph_objs as go
import plotly.io as pio
from fastapi.middleware.cors import CORSMiddleware
from routers.Graph import router as graphRouter
from fastapi.responses import JSONResponse
from routers.Users import router as UserRouter
from routers.Contratistas import router as ContrastRouter
from routers.Desviaciones import router as DesviacionRouter
from routers.Capacitacion import router as CapacitacionRouter
from routers.Cronograma import router as CronogramaRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi import HTTPException

import os 



app = FastAPI()
app.include_router(graphRouter)
app.include_router(UserRouter)
app.include_router(ContrastRouter)
app.include_router(DesviacionRouter)
app.include_router(CapacitacionRouter)
app.include_router(CronogramaRouter)
app.mount("/File", StaticFiles(directory="File"), name="File")

app.add_middleware(
    CORSMiddleware,
    # Cambia esto por los dominios permitidos en producción
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
