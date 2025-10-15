from fastapi import APIRouter, HTTPException
from typing import List
import uuid
import crud
from models import Appointment, AppointmentCreate

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.post("/", response_model=Appointment, status_code=201)
def create_new_appointment(appointment: AppointmentCreate):
    try:
        return crud.create_appointment(appointment=appointment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[Appointment])
def read_appointments(skip: int = 0, limit: int = 100):
    return crud.get_appointments(skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=Appointment)
def read_appointment(appointment_id: uuid.UUID):
    db_appointment = crud.get_appointment(appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment