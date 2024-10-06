from fastapi import FastAPI
import plotly.graph_objs as go
import plotly.io as pio
from fastapi.middleware.cors import CORSMiddleware
from routers.Graph import router as graphRouter
from fastapi.responses import JSONResponse
from routers.Users import router as UserRouter
from routers.Contratistas import router as ContrastRouter
app = FastAPI()

app.include_router(graphRouter)
app.include_router(UserRouter)
app.include_router(ContrastRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por los dominios permitidos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

