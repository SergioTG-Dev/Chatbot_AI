from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from db.supabase_client import supabase
from schemas.department import Department, DepartmentCreate, DepartmentUpdate
from schemas.procedure import Procedure

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(
    department: DepartmentCreate, 
):
    """
    Crea un nuevo departamento. Solo un administrador puede realizar esta acción.
    """
    response = supabase.table("departments").insert(department.model_dump()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating department")
    return response.data[0]

@router.get("/", response_model=List[Department])
def read_departments(
    skip: int = 0, 
    limit: int = 100
    # _user: User = Depends(get_current_user) # <-- Descomenta si quieres que solo usuarios logueados vean la lista
):
    """
    Obtiene la lista de todos los departamentos.
    """
    response = supabase.table("departments").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{department_id}", response_model=Department)
def read_department(department_id: UUID):
    """
    Obtiene un departamento por su ID.
    """
    response = supabase.table("departments").select("*").eq("id", department_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Department not found")
    return response.data[0]

@router.get("/{department_id}/procedures", response_model=List[Procedure])
def get_department_procedures(department_id: UUID):
    """
    Obtiene la lista de trámites (procedimientos) que ofrece un departamento específico.
    """
    response = supabase.table("procedures").select("*").eq("department_id", department_id).execute()
    if not response.data:
        # No es un error 404, simplemente el departamento no tiene procedimientos
        return []
    return response.data

@router.put("/{department_id}", response_model=Department)
def update_department(
    department_id: UUID, 
    department_update: DepartmentUpdate
    #_admin: Dep = Depends(get_current_admin) # <-- SOLO ADMIN
):
    """
    Actualiza un departamento. Solo un administrador puede realizar esta acción.
    """
    db_department = supabase.table("departments").select("*").eq("id", department_id).execute()
    if not db_department.data:
        raise HTTPException(status_code=404, detail="Department not found")
    
    response = supabase.table("departments").update(department_update.model_dump(exclude_unset=True)).eq("id", department_id).execute()
    return response.data[0]

@router.delete("/{department_id}")
def delete_department(
    department_id: UUID,
    #_admin: Dep = Depends(get_current_admin) # <-- SOLO ADMIN
):
    """
    Elimina un departamento. Solo un administrador puede realizar esta acción.
    Los funcionarios asignados a este departamento quedarán sin departamento (department_id = NULL).
    """
    db_department = supabase.table("departments").select("*").eq("id", department_id).execute()
    if not db_department.data:
        raise HTTPException(status_code=404, detail="Department not found")
    
    supabase.table("departments").delete().eq("id", department_id).execute()
    return {"message": "Department deleted successfully"}