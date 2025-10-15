# API de Gestión Gubernamental (Argentina)

API RESTful desarrollada con FastAPI y Supabase para la gestión de ciudadanos, tickets de solicitud y turnos para trámites.

## Características

-   **Gestión de Ciudadanos (CRUD):** Crear, leer y gestionar los datos de los ciudadanos.
-   **Sistema de Tickets:** Crear solicitudes (ej. reparación de calles). Se valida que el DNI exista.
-   **Sistema de Turnos:** Programar turnos para trámites (ej. pasaporte, carnet de conducir). Se valida que el DNI exista.
-   **Documentación Automática:** Generada con Swagger UI y ReDoc.
-   **Base de Datos:** Usando Supabase como Backend-as-a-Service.

## Tecnologías

-   [FastAPI](https://fastapi.tiangolo.com/)
-   [Supabase](https://supabase.com/)
-   [Pydantic](https://pydantic-docs.helpmanual.io/)
-   [Uvicorn](https://www.uvicorn.org/)

## Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd gestion-gob-api
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Supabase:**
    -   Crea un nuevo proyecto en [Supabase](https://supabase.com/).
    -   Ve a `Settings > API` para obtener tu `URL` y `service_role KEY`.
    -   En el `SQL Editor`, ejecuta las consultas SQL proporcionadas en la documentación del proyecto para crear las tablas `tickets` y `appointments`.

5.  **Configurar variables de entorno:**
    -   Crea un archivo `.env` en la raíz del proyecto.
    -   Añade tus credenciales de Supabase:
        ```
        SUPABASE_URL="TU_SUPABASE_URL"
        SUPABASE_KEY="TU_SUPABASE_SERVICE_ROLE_KEY"
        ```

## Ejecución

Inicia el servidor de desarrollo:

```bash
uvicorn main:app --reload