from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TurnoBase(BaseModel):
    procedure_type: str
    scheduled_at: datetime

class TurnoCreate(TurnoBase):
    citizen_dni: str

class Turno(TurnoBase):
    id: UUID
    citizen_id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True