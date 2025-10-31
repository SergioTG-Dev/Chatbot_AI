from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..db.supabase_client import supabase
from ..schemas.official import Official

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Official:
    """
    Dependencia para obtener el usuario actual a partir del token JWT de Supabase.
    Verifica el token y busca los detalles del funcionario en la base de datos.
    """
    token = credentials.credentials
    try:
        # Verifica el token con Supabase y obtiene los datos del usuario de auth.users
        auth_user = supabase.auth.get_user(token)
        user_id = auth_user.user.id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Busca al funcionario en nuestra tabla pública usando el ID de auth.users
    official_response = supabase.table("officials").select("*").eq("id", user_id).execute()
    
    if not official_response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in officials table"
        )
        
    return Official(**official_response.data[0])

async def get_current_admin(current_user: Official = Depends(get_current_user)) -> Official:
    """
    Dependencia para asegurar que el usuario actual tiene rol de 'admin'.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user