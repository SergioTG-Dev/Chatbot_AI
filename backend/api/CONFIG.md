# Configuración de entorno de la API

Esta API requiere Supabase SIEMPRE activo. Asegúrate de configurar correctamente las variables de entorno.

## Ubicación del archivo `.env`

- Usa `backend/api/src/.env`. El loader de `pydantic-settings` está configurado para leer ese archivo.

## Variables requeridas

Copiar y completar:

```
SUPABASE_URL="https://<TU-PROJECT-REF>.supabase.co"
SUPABASE_KEY="<OPCIONAL: ANON O PUBLISHABLE>"
SUPABASE_SERVICE_ROLE_KEY="<SERVICE_ROLE_KEY - NO EXPONER EN FRONTEND>"
REDIS_URL="redis://localhost:6379"
SECRET_KEY="<clave-secreta-para-JWT>"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- Obtén `SUPABASE_URL` y claves en `Settings > API` del proyecto Supabase.
- La API usa `SUPABASE_SERVICE_ROLE_KEY` para operaciones sobre tablas; `SUPABASE_KEY` debe existir para validación.

## Arranque recomendado

```
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend (referencia)

- En `front/.env.local` (o variables de entorno):

```
NEXT_PUBLIC_SUPABASE_URL="https://<TU-PROJECT-REF>.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="<ANON KEY>"
```

No expongas `SERVICE_ROLE_KEY` en el frontend.