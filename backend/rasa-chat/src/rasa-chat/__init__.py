import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Opcional: debug, imprimir si quieres verificar
print("Twilio SID cargado:", os.getenv("TWILIO_ACCOUNT_SID"))
