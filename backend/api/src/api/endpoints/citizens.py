from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from db.supabase_client import supabase
from schemas.citizen import Citizen, CitizenCreate, CitizenUpdate
from schemas.ticket import Ticket
from schemas.turno import Turno

router = APIRouter(prefix="/citizens", tags=["Citizens"])

@router.post("/", response_model=Citizen, status_code=status.HTTP_201_CREATED)
def create_citizen(citizen: CitizenCreate):
    # Verificar si el DNI ya existe
    existing = supabase.table("citizens").select("id").eq("dni", citizen.dni).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="DNI already registered")
    
    response = supabase.table("citizens").insert(citizen.model_dump()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating citizen")
    return response.data[0]

@router.get("/", response_model=List[Citizen])
def read_citizens(skip: int = 0, limit: int = 100):
    response = supabase.table("citizens").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{dni}", response_model=Citizen)
def read_citizen_by_dni(dni: str):
    response = supabase.table("citizens").select("*").eq("dni", dni).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return response.data[0]

@router.get("/{dni}/tickets", response_model=List[Ticket])
def get_citizen_tickets(dni: str):
    """
    Obtiene todos los tickets asociados a un ciudadano por su DNI.
    """
    citizen = supabase.table("citizens").select("id").eq("dni", dni).execute()
    if not citizen.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
    
    citizen_id = citizen.data[0]['id']
    response = supabase.table("tickets").select("*, procedures(name)").eq("citizen_id", citizen_id).execute()
    return response.data

@router.get("/{dni}/turnos", response_model=List[Turno])
def get_citizen_turnos(dni: str):
    """
    Obtiene todos los turnos asociados a un ciudadano por su DNI.
    """
    citizen = supabase.table("citizens").select("id").eq("dni", dni).execute()
    if not citizen.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
        
    citizen_id = citizen.data[0]['id']
    response = supabase.table("turnos").select("*, procedures(name, departments(name))").eq("citizen_id", citizen_id).execute()
    return response.data

@router.put("/{dni}", response_model=Citizen)
def update_citizen(dni: str, citizen_update: CitizenUpdate):
    db_citizen = supabase.table("citizens").select("*").eq("dni", dni).execute()
    if not db_citizen.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
    
    response = supabase.table("citizens").update(citizen_update.model_dump(exclude_unset=True)).eq("dni", dni).execute()
    return response.data[0]

@router.delete("/{dni}")
def delete_citizen(dni: str):
    db_citizen = supabase.table("citizens").select("*").eq("dni", dni).execute()
    if not db_citizen.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
    
    supabase.table("citizens").delete().eq("dni", dni).execute()
    return {"message": "Citizen deleted successfully"}