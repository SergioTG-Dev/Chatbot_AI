from fastapi import APIRouter
from endpoints import citizens, officials, tickets, turnos, chat, departments, procedures
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(citizens.router)
api_router.include_router(departments.router)
api_router.include_router(officials.router)
api_router.include_router(tickets.router)
api_router.include_router(turnos.router)
api_router.include_router(procedures.router)
api_router.include_router(chat.router)