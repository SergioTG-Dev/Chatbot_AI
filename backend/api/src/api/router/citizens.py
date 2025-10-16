from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
import crud
from models import Citizen, CitizenCreate

router = APIRouter(
    prefix="/citizens",
    tags=["Citizens"]
)

@router.post("/", response_model=Citizen, status_code=201)
def create_new_citizen(citizen: CitizenCreate):
    # Verificar si el DNI ya existe
    db_citizen = crud.get_citizen_by_dni(citizen.dni)
    if db_citizen:
        raise HTTPException(status_code=400, detail=f"El ciudadano con DNI {citizen.dni} ya está registrado.")
    return crud.create_citizen(citizen=citizen)

@router.get("/", response_model=List[Citizen])
def read_citizens(skip: int = 0, limit: int = 100):
    citizens = crud.get_citizens(skip=skip, limit=limit)
    return citizens

@router.get("/{citizen_id}", response_model=Citizen)
def read_citizen(citizen_id: uuid.UUID):
    db_citizen = crud.get_citizen(citizen_id=citizen_id)
    if db_citizen is None:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return db_citizen