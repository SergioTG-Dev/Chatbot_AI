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
    - Ejecuta el script SQL proporcionado en la documentación del proyecto en el editor SQL de tu proyecto Supabase para crear las tablas necesarias.

### 3. Poblar la Base de Datos

Para llenar la base de datos con datos de prueba, ejecuta el seeder:

```bash
poetry run python -m app.utils.seeder