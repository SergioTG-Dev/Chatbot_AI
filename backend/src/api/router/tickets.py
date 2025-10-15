from fastapi import APIRouter, HTTPException
from typing import List
import uuid
import crud
from models import Ticket, TicketCreate

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/", response_model=Ticket, status_code=201)
def create_new_ticket(ticket: TicketCreate):
    try:
        return crud.create_ticket(ticket=ticket)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[Ticket])
def read_tickets(skip: int = 0, limit: int = 100):
    return crud.get_tickets(skip=skip, limit=limit)

@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: uuid.UUID):
    db_ticket = crud.get_ticket(ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}/status", response_model=Ticket)
def update_ticket_status(ticket_id: uuid.UUID, status: str):
    db_ticket = crud.update_ticket_status(ticket_id=ticket_id, status=status)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket