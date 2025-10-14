from fastapi import FastAPI
from routers import citizens, tickets, appointments

app = FastAPI(
    title="API de Gestión Gubernamental",
    description="API para la gestión de ciudadanos, tickets de solicitud y turnos para trámites del Gobierno de Argentina.",
    version="1.0.0",
)

app.include_router(citizens.router)
app.include_router(tickets.router)
app.include_router(appointments.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Gestión Gubernamental. Visita /docs para ver la documentación."}