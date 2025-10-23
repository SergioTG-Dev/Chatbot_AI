from supabase import create_client
from supabase.lib.client_options import ClientOptions
from core.config import settings

supabase = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_SERVICE_ROLE_KEY,
    options=ClientOptions(        
        auto_refresh_token=False,        
        persist_session=False,    
    ))

admin_auth_client = supabase.auth.admin