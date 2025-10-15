from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

# --- Citizens ---
class CitizenBase(BaseModel):
    dni: str
    first_name: str
    last_name: str

class CitizenCreate(CitizenBase):
    pass

class Citizen(CitizenBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

# --- Tickets ---
class TicketBase(BaseModel):
    subject: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    citizen_dni: str # El usuario proporciona el DNI, no el ID

class Ticket(TicketBase):
    id: uuid.UUID
    citizen_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# --- Appointments ---
class AppointmentBase(BaseModel):
    procedure_type: str
    appointment_datetime: datetime
    office_location: str

class AppointmentCreate(AppointmentBase):
    citizen_dni: str # El usuario proporciona el DNI

class Appointment(AppointmentBase):
    id: uuid.UUID
    citizen_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True