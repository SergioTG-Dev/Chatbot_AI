param(
    [int]$RasaPort = 5005,
    [int]$ActionsPort = 5055,
    [int]$FrontendPort = 3000,
    [int]$FastApiPort = 8000
)

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$backendRasa = Join-Path $root "backend\rasa-chat"
$actionsDir = Join-Path $backendRasa "src\rasa-chat"
$backendApi = Join-Path $root "backend\api"
$frontDir = Join-Path $root "front"

# 1) FastAPI (Backend REST) – requiere Poetry y archivo .env válido
Start-Process -FilePath "powershell" -ArgumentList @('-NoExit','-Command',"cd $backendApi; poetry install; poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port $FastApiPort")

# 2) Rasa Action Server – apuntando al FastAPI local
Start-Process -FilePath "powershell" -ArgumentList @('-NoExit','-Command',"cd $actionsDir; $env:FASTAPI_URL='http://127.0.0.1:$FastApiPort'; poetry install; poetry run rasa run actions --port $ActionsPort --debug")

# 3) Rasa Server – con endpoint de acciones y FASTAPI_URL configurado
Start-Process -FilePath "powershell" -ArgumentList @('-NoExit','-Command',"cd $backendRasa; $env:ACTION_ENDPOINT_URL='http://127.0.0.1:$ActionsPort/webhook'; $env:FASTAPI_URL='http://127.0.0.1:$FastApiPort'; poetry install; poetry run rasa run -m models --enable-api --cors '*' --endpoints src/rasa-chat/endpoints.yml --interface 0.0.0.0 --port $RasaPort --debug")

# 4) Frontend – exportar URLs para hablar con Rasa y FastAPI
Start-Process -FilePath "powershell" -ArgumentList @('-NoExit','-Command',"cd $frontDir; $env:NEXT_PUBLIC_RASA_API_URL='http://127.0.0.1:$RasaPort/webhooks/rest/webhook'; $env:NEXT_PUBLIC_API_BASE_URL='http://127.0.0.1:$FastApiPort'; npm install; npm run dev -- --port $FrontendPort")