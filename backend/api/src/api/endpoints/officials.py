from fastapi import APIRouter,Depends, HTTPException, status
from typing import List
from uuid import UUID
from db.supabase_client import supabase, admin_auth_client
from schemas.official import Official, OfficialCreate, OfficialCreateWithAuth, OfficialUpdate
from core.deps import get_current_admin, get_current_user

router = APIRouter(prefix="/officials", tags=["Officials"])

@router.post("/", response_model=Official, status_code=status.HTTP_201_CREATED)
def create_official(official_data: OfficialCreateWithAuth
    #, _admin: Official = Depends(get_current_admin)
):

    """
    Crea un nuevo funcionario. Este endpoint está protegido y solo puede ser usado por un admin.
    Crea el usuario en auth.users y el perfil en public.officials.
    """
    try:
        user_response = admin_auth_client.create_user(
            {
                "email": official_data.email,
                "password": official_data.password,
                "email_confirm": True
            }
        )
        new_user_id = user_response.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user in auth.users: {e}"
        )
    
    official_profile_data = official_data.model_dump(mode="json",exclude={"email", "password"})
    official_profile_data["id"] = str(new_user_id)

    response = supabase.table("officials").insert(official_profile_data).execute()

    if not response.data:
        admin_auth_client.delete_user(new_user_id)
        raise HTTPException(status_code=400, detail="Error creating official profile after user creation.")

    return response.data[0]

@router.get("/", response_model=List[Official])
def read_officials(
    skip: int = 0, 
    limit: int = 100,
    # _current_user: Official = Depends(get_current_user)
    ):
    response = supabase.table("officials").select("*").range(skip, skip + limit - 1).execute()
    return response.data

@router.get("/{official_id}", response_model=Official)
def read_official(official_id: UUID):
    response = supabase.table("officials").select("*").eq("id", official_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Official not found")
    return response.data[0]

@router.put("/{official_id}", response_model=Official)
def update_official(official_id: UUID, official_update: OfficialUpdate):
    db_official = supabase.table("officials").select("*").eq("id", official_id).execute()
    if not db_official.data:
        raise HTTPException(status_code=404, detail="Official not found")
    
    response = supabase.table("officials").update(official_update.model_dump(mode='json', exclude_unset=True)).eq("id", official_id).execute()
    return response.data[0]

@router.delete("/{official_id}")
def delete_official(official_id: UUID):
    db_official = supabase.table("officials").select("*").eq("id", official_id).execute()

    if not db_official.data:
        raise HTTPException(status_code=404, detail="Official not found")
    
    supabase.table("officials").delete().eq("id", official_id).execute()
    return {"message": "Official deleted successfully"}