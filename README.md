# Chatbot_AI
Chatbot IA para Atención Ciudadana

## Inicio Rápido

- Requisitos:
  - `Python 3.10` y `Poetry` en el `PATH`.
  - `Node.js` 18+ y `npm`.
  - Archivo `.env` en `backend\api` (puedes copiar el ejemplo):
    - `cd backend\api`
    - `copy .env.example .env`
    - Edita `backend\api\.env` con tus valores.

### Opción 1: Script que levanta todo

- Desde la raíz del repo:
- `powershell -ExecutionPolicy Bypass -File .\scripts\start-chatbot.ps1`
- Puertos por defecto:
  - FastAPI `http://127.0.0.1:8000`
  - Rasa Actions `http://127.0.0.1:5055`
  - Rasa Server `http://127.0.0.1:5005`
  - Frontend `http://127.0.0.1:3000`
- Puertos personalizados (ejemplo):
- `powershell -ExecutionPolicy Bypass -File .\scripts\start-chatbot.ps1 -RasaPort 5006 -ActionsPort 5056 -FrontendPort 3001 -FastApiPort 8001`

### Opción 2: Levantar servicios manualmente

- Backend FastAPI:
  - `cd .\backend\api`
  - `poetry install`
  - `poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`
- Rasa Action Server:
  - `cd .\backend\rasa-chat\src\rasa-chat`
  - `$env:FASTAPI_URL="http://127.0.0.1:8000"`
  - `poetry install`
  - `poetry run rasa run actions --port 5055 --debug`
- Rasa Server:
  - `cd .\backend\rasa-chat`
  - `$env:ACTION_ENDPOINT_URL="http://127.0.0.1:5055/webhook"`
  - `$env:FASTAPI_URL="http://127.0.0.1:8000"`
  - `poetry install`
  - `poetry run rasa run -m models --enable-api --cors "*" --endpoints src/rasa-chat/endpoints.yml --interface 0.0.0.0 --port 5005 --debug`
- Frontend (Next.js):
  - `cd .\front`
  - `$env:NEXT_PUBLIC_RASA_API_URL="http://127.0.0.1:5005/webhooks/rest/webhook"`
  - `$env:NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000"`
  - `npm install`
  - `npm run dev -- --port 3000`

### Comprobaciones y endpoints útiles

- Frontend: `http://localhost:3000`
- FastAPI docs: `http://localhost:8000/docs`
- Action Server: `http://localhost:5055/health`
- Rasa status: `http://localhost:5005/status`
- Webhook REST: `http://localhost:5005/webhooks/rest/webhook`
- Probar webhook (PowerShell):
- `Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5005/webhooks/rest/webhook -ContentType 'application/json' -Body '{"sender":"test","message":"Hola"}'`

### Problemas comunes y soluciones

- Poetry no arranca / error `No module named 'packaging.metadata'`:
  - `python -m pip install --upgrade pip setuptools wheel packaging`
  - Verifica: `poetry --version`
- Frontend “Missing script: dev”:
  - En `front\package.json` existe `"dev": "next dev --turbopack"`. Ejecuta `npm install` y luego `npm run dev -- --port 3000`.
- Puertos ocupados:
  - Cambia puertos con parámetros del script o ajusta los `--port` manuales.

### Cómo detener servicios

- Si usaste el script: cierra las ventanas de PowerShell que se abrieron.
- Si los levantaste manualmente: `Ctrl+C` en cada terminal.
