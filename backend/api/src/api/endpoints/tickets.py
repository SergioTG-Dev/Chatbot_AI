from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from db.supabase_client import supabase
from schemas.ticket import Ticket, TicketCreate, TicketUpdate
from endpoints.citizens import read_citizen_by_dni

router = APIRouter(prefix="/tickets", tags=["Tickets"])

def get_citizen_by_dni(dni: str):
    try:
        return read_citizen_by_dni(dni)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail="Citizen with given DNI not found. Cannot create ticket.")

@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate):
    citizen = get_citizen_by_dni(ticket.citizen_dni)
    
    ticket_data = ticket.model_dump(mode="json", exclude={"citizen_dni"})
    ticket_data["citizen_id"] = str(citizen["id"])
    
    response = supabase.table("tickets").insert(ticket_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating ticket")
    return response.data[0]

@router.get("/", response_model=List[Ticket])
def read_tickets(skip: int = 0, limit: int = 100):
    response = supabase.table("tickets").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: UUID):
    response = supabase.table("tickets").select("*").eq("id", ticket_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return response.data[0]

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: UUID, ticket_update: TicketUpdate):
    db_ticket = supabase.table("tickets").select("*").eq("id", ticket_id).execute()
    if not db_ticket.data:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    response = supabase.table("tickets").update(ticket_update.model_dump(exclude_unset=True)).eq("id", ticket_id).execute()
    return response.data[0]

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: UUID):
    db_ticket = supabase.table("tickets").select("*").eq("id", ticket_id).execute()
    if not db_ticket.data:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    supabase.table("tickets").delete().eq("id", ticket_id).execute()
    return {"message": "Ticket deleted successfully"}