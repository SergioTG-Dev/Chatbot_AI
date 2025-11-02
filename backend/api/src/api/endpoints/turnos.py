from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from uuid import UUID
from datetime import datetime
from ..db.supabase_client import supabase
from ..schemas.turno import Turno, TurnoCreate, TurnoUpdate
from .tickets import get_citizen_by_dni

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.post("/", response_model=Turno, status_code=status.HTTP_201_CREATED)
def create_turno(turno: TurnoCreate):
    citizen = get_citizen_by_dni(turno.citizen_dni)
    
    # Verificar que el procedimiento existe
    procedure = supabase.table("procedures").select("*").eq("id", turno.procedure_id).execute()
    if not procedure.data:
        raise HTTPException(status_code=404, detail="Procedure not found")

    # Serializar a JSON para evitar problemas con UUID/datetime
    turno_data = turno.model_dump(mode="json", exclude={"citizen_dni"})
    # `get_citizen_by_dni` devuelve un dict; acceder por clave
    turno_data["citizen_id"] = citizen["id"]
    # Asegurar estado por defecto si la BD no retorna default
    if "status" not in turno_data or not turno_data["status"]:
        turno_data["status"] = "programado"
    
    response = supabase.table("turnos").insert(turno_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating turno")
    inserted_id = response.data[0]["id"]
    # Leer la fila completa para asegurar defaults (como status)
    final = supabase.table("turnos").select("*").eq("id", inserted_id).execute()
    return final.data[0]

@router.get("/", response_model=List[Turno])
def read_turnos(skip: int = 0, limit: int = 100):
    response = supabase.table("turnos").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/available-slots", response_model=List[datetime])
def get_available_slots(
    procedure_id: UUID,
    target_date: date = Query(..., description="Fecha a consultar en formato YYYY-MM-DD")
):
    """
    Devuelve una lista de horas disponibles para un procedimiento en una fecha específica.
    """
    # 1. Obtener detalles del procedimiento (duración)
    procedure_response = supabase.table("procedures").select("duration_minutes").eq("id", procedure_id).execute()
    if not procedure_response.data:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    duration = procedure_response.data[0]['duration_minutes']
    
    # 2. Definir horario laboral (ej: 9:00 a 17:00)
    start_time = datetime.combine(target_date, datetime.min.time()).replace(hour=9)
    end_time = datetime.combine(target_date, datetime.min.time()).replace(hour=17)
    
    # 3. Generar todos los posibles slots del día
    possible_slots = []
    current_time = start_time
    while current_time + timedelta(minutes=duration) <= end_time:
        possible_slots.append(current_time)
        current_time += timedelta(minutes=duration)

    # 4. Obtener los turnos ya ocupados para ese procedimiento y fecha
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())
    
    booked_turnos_response = supabase.table("turnos").select("scheduled_at").eq("procedure_id", procedure_id).gte("scheduled_at", start_of_day.isoformat()).lte("scheduled_at", end_of_day.isoformat()).in_("status", ["programado", "completado"]).execute()
    
    booked_slots = {datetime.fromisoformat(t['scheduled_at'].replace('Z', '+00:00')) for t in booked_turnos_response.data}

    # 5. Calcular slots disponibles
    available_slots = [slot for slot in possible_slots if slot not in booked_slots]
    
    return available_slots

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

@router.put("/{turno_id}", response_model=Turno)
def update_turno(turno_id: UUID, turno_update: TurnoUpdate):
    db_turno = supabase.table("turnos").select("*").eq("id", turno_id).execute()
    if not db_turno.data:
        raise HTTPException(status_code=404, detail="Turno not found")

    # Solo actualiza los campos proporcionados
    update_data = turno_update.model_dump(exclude_unset=True)
    if not update_data:
        return db_turno.data[0]

    response = supabase.table("turnos").update(update_data).eq("id", turno_id).execute()
    return response.data[0]

@router.delete("/{turno_id}")
def delete_turno(turno_id: UUID):
    db_turno = supabase.table("turnos").select("*").eq("id", turno_id).execute()
    if not db_turno.data:
        raise HTTPException(status_code=404, detail="Turno not found")

    supabase.table("turnos").delete().eq("id", turno_id).execute()
    return {"message": "Turno deleted successfully"}