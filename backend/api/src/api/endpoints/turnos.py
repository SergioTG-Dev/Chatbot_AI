from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from datetime import datetime
from db.supabase_client import supabase
from schemas.turno import Turno, TurnoCreate
from endpoints.tickets import get_citizen_by_dni

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.post("/", response_model=Turno, status_code=status.HTTP_201_CREATED)
def create_turno(turno: TurnoCreate):
    citizen = get_citizen_by_dni(turno.citizen_dni)
    
    turno_data = turno.model_dump(mode="json", exclude={"citizen_dni"})
    turno_data["citizen_id"] = str(citizen['id'])
    
    response = supabase.table("turnos").insert(turno_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating turno")
    return response.data[0]

@router.get("/", response_model=List[Turno])
def read_turnos(skip: int = 0, limit: int = 100):
    response = supabase.table("turnos").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{turno_id}", response_model=Turno)
def read_turno(turno_id: UUID):
    response = supabase.table("turnos").select("*").eq("id", turno_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Turno not found")
    return response.data[0]

@router.put("/{turno_id}/cancelar", response_model=Turno)
def cancel_turno(turno_id: UUID):
    db_turno = supabase.table("turnos").select("*").eq("id", turno_id).execute()
    if not db_turno.data:
        raise HTTPException(status_code=404, detail="Turno not found")
    
    response = supabase.table("turnos").update({"status": "cancelado"}).eq("id", turno_id).execute()
    return response.data[0]