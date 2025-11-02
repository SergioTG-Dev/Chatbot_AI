from turtle import mode
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from ..db.supabase_client import supabase
from ..schemas.procedure import Procedure, ProcedureCreate, ProcedureUpdate

router = APIRouter(prefix="/procedures", tags=["Procedures"])

@router.post("/", response_model=Procedure, status_code=status.HTTP_201_CREATED)
def create_procedure(procedure: ProcedureCreate):
    response = supabase.table("procedures").insert(procedure.model_dump(mode="json")).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating procedure")
    return response.data[0]

@router.get("/", response_model=List[Procedure])
def read_procedures(skip: int = 0, limit: int = 100, department_id: Optional[UUID] = Query(default=None)):
    if department_id is not None:
        response = supabase.table("procedures").select("*, departments(name)").eq("department_id", str(department_id)).execute()
    else:
        response = supabase.table("procedures").select("*, departments(name)").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{procedure_id}", response_model=Procedure)
def read_procedure(procedure_id: UUID):
    response = supabase.table("procedures").select("*, departments(name)").eq("id", procedure_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return response.data[0]

@router.put("/{procedure_id}", response_model=Procedure)
def update_procedure(procedure_id: UUID, procedure_update: ProcedureUpdate):
    response = supabase.table("procedures").update(procedure_update.model_dump(exclude_unset=True)).eq("id", procedure_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return response.data[0]

@router.delete("/{procedure_id}")
def delete_procedure(procedure_id: UUID):
    supabase.table("procedures").delete().eq("id", procedure_id).execute()
    return {"message": "Procedure deleted successfully"}