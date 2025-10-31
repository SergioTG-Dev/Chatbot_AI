# API de Gestión Gubernamental

API RESTful para la gestión de tickets, turnos y un sistema de chat en tiempo real para el Gobierno de Argentina.

## Tecnologías

- **Backend**: FastAPI
- **Base de Datos**: Supabase (PostgreSQL)
- **Caching/Real-time**: Redis
- **Gestión de Dependencias**: Poetry
- **Pruebas**: Pytest

## Configuración y Ejecución

### 1. Prerrequisitos

- Python 3.10+
- Poetry
- Redis corriendo en `localhost:6379`
- Una cuenta y proyecto en [Supabase](https://supabase.com/).

### 2. Configuración del Proyecto

1.  **Clona el repositorio:**
    ```bash
    git clone <tu-repo-url>
    cd gestion-gubernamental
    ```

2.  **Instala las dependencias con Poetry:**
    ```bash
    poetry install
    ```

3.  **Configura las variables de entorno:**
    - Copia `.env.example` a `.env` (o crea el archivo `.env`).
    - Completa los valores de `SUPABASE_URL`, `SUPABASE_KEY`, `REDIS_URL` y `SECRET_KEY`.

4.  **Configura la Base de Datos en Supabase:**
    - Abre el editor SQL de tu proyecto Supabase y ejecuta el archivo `backend/api/codigo.sql` para crear las tablas necesarias (incluida `faqs_gcba`).

### 3. Poblar la Base de Datos

Para llenar la base de datos:

- Datos de prueba (ciudadanos, tickets, turnos, etc.):
  ```bash
  poetry run python src/api/seed_data.py
  ```

- Base de conocimiento de Preguntas Frecuentes (FAQs):
  ```bash
  poetry run python src/api/seed_faqs.py
  ```

Si la tabla `faqs_gcba` no existe, asegúrate de ejecutar `backend/api/codigo.sql` primero.