import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("Faltan las variables de entorno SUPABASE_URL o SUPABASE_KEY")

supabase: Client = create_client(URL, KEY)