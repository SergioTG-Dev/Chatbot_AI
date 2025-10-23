from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: UUID

class TicketCreate(TicketBase):
    citizen_dni: str # Se usa el DNI para identificar al ciudadano

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_official_id: Optional[UUID] = None

class Ticket(TicketBase):
    id: UUID
    citizen_id: UUID
    assigned_official_id: Optional[UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True