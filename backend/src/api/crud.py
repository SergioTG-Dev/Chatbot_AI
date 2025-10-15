import uuid
from typing import List, Optional
from database import supabase
from models import CitizenCreate, TicketCreate, AppointmentCreate, Citizen, Ticket, Appointment

# --- Citizens CRUD ---
def get_citizen_by_dni(dni: str) -> Optional[Citizen]:
    response = supabase.table("citizens").select("*").eq("dni", dni).execute()
    if response.data:
        return Citizen(**response.data[0])
    return None

def create_citizen(citizen: CitizenCreate) -> Citizen:
    response = supabase.table("citizens").insert(citizen.dict()).execute()
    return Citizen(**response.data[0])

def get_citizens(skip: int = 0, limit: int = 100) -> List[Citizen]:
    response = supabase.table("citizens").select("*").range(skip, skip + limit - 1).execute()
    return [Citizen(**item) for item in response.data]

def get_citizen(citizen_id: uuid.UUID) -> Optional[Citizen]:
    response = supabase.table("citizens").select("*").eq("id", str(citizen_id)).execute()
    if response.data:
        return Citizen(**response.data[0])
    return None

# --- Tickets CRUD ---
def create_ticket(ticket: TicketCreate) -> Ticket:
    citizen = get_citizen_by_dni(ticket.citizen_dni)
    if not citizen:
        raise ValueError(f"El ciudadano con DNI {ticket.citizen_dni} no existe.")
    
    ticket_data = ticket.dict(exclude={"citizen_dni"})
    ticket_data["citizen_id"] = citizen.id
    
    response = supabase.table("tickets").insert(ticket_data).execute()
    return Ticket(**response.data[0])

def get_tickets(skip: int = 0, limit: int = 100) -> List[Ticket]:
    response = supabase.table("tickets").select("*").range(skip, skip + limit - 1).execute()
    return [Ticket(**item) for item in response.data]

def get_ticket(ticket_id: uuid.UUID) -> Optional[Ticket]:
    response = supabase.table("tickets").select("*").eq("id", str(ticket_id)).execute()
    if response.data:
        return Ticket(**response.data[0])
    return None

def update_ticket_status(ticket_id: uuid.UUID, status: str) -> Optional[Ticket]:
    response = supabase.table("tickets").update({"status": status}).eq("id", str(ticket_id)).execute()
    if response.data:
        return Ticket(**response.data[0])
    return None

# --- Appointments CRUD ---
def create_appointment(appointment: AppointmentCreate) -> Appointment:
    citizen = get_citizen_by_dni(appointment.citizen_dni)
    if not citizen:
        raise ValueError(f"El ciudadano con DNI {appointment.citizen_dni} no existe.")

    appointment_data = appointment.dict(exclude={"citizen_dni"})
    appointment_data["citizen_id"] = citizen.id

    response = supabase.table("appointments").insert(appointment_data).execute()
    return Appointment(**response.data[0])

def get_appointments(skip: int = 0, limit: int = 100) -> List[Appointment]:
    response = supabase.table("appointments").select("*").range(skip, skip + limit - 1).execute()
    return [Appointment(**item) for item in response.data]

def get_appointment(appointment_id: uuid.UUID) -> Optional[Appointment]:
    response = supabase.table("appointments").select("*").eq("id", str(appointment_id)).execute()
    if response.data:
        return Appointment(**response.data[0])
    return None