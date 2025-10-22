from fastapi import FastAPI
from v1.api import api_router
from core.config import settings

app = FastAPI(
    title="API de Gestión Gubernamental",
    description="API para la gestión de tickets, turnos y chat del Gobierno de Argentina.",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Gestión Gubernamental de Argentina"}

# Para ejecutar: poetry run start