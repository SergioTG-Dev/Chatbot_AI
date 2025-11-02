from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from .v1.api import api_router
from .core.config import settings

app = FastAPI(
    title="API de Gestión Gubernamental",
    description="API para la gestión de tickets, turnos y chat del Gobierno de Argentina.",
    version="1.0.0",
)

app.include_router(api_router)

# CORS para permitir llamadas desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Gestión Gubernamental de Argentina"}

# Para ejecutar: poetry run start

# Exponer métricas Prometheus en /metrics e instrumentar todas las rutas
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Endpoint de depuración para listar rutas registradas en tiempo real
@app.get("/debug/routes", tags=["Debug"])
def list_routes():
    try:
        rutas = []
        for route in app.routes:
            rutas.append({
                "path": getattr(route, "path", ""),
                "name": getattr(route, "name", ""),
                "methods": list(getattr(route, "methods", []) or []),
            })
        return {"routes": rutas, "count": len(rutas)}
    except Exception as e:
        return {"error": str(e)}

# Imprimir rutas registradas al inicio para diagnóstico
@app.on_event("startup")
async def print_registered_routes():
    try:
        print("=== Rutas registradas ===")
        for route in app.routes:
            try:
                print(f"PATH: {getattr(route, 'path', '')} | NAME: {getattr(route, 'name', '')}")
            except Exception:
                pass
        print("=== Fin de rutas ===")
    except Exception as e:
        print(f"Error imprimiendo rutas: {e}")