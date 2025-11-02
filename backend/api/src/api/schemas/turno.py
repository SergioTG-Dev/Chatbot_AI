from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class TurnoStatus(str, Enum):
    abierto = "abierto"
    programado = "programado"
    en_progreso = "en_progreso"
    resuelto = "resuelto"
    cerrado = "cerrado"
    cancelado = "cancelado"

class TurnoBase(BaseModel):
    procedure_id: UUID
    scheduled_at: datetime

class TurnoCreate(TurnoBase):
    citizen_dni: str

class TurnoUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: TurnoStatus | None = None

class Turno(TurnoBase):
    id: UUID
    citizen_id: UUID
    status: TurnoStatus
    created_at: datetime

    class Config:
        from_attributes = True